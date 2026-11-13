'use strict';

const fs = require('node:fs');
const path = require('node:path');
const readline = require('node:readline');
const { spawn } = require('node:child_process');

async function run() {
  const [cli, job, planPath] = process.argv.slice(2);
  if (!cli || !job || !planPath || !path.isAbsolute(cli) || !path.isAbsolute(job)) {
    throw new Error('Usage: node solidcraft-mcp.cjs <absolute-cli-path> <absolute-job-folder> <plan.json>');
  }
  if (!fs.statSync(job).isDirectory()) throw new Error('The job folder must exist');

  const plan = JSON.parse(fs.readFileSync(planPath, 'utf8').replace(/^\uFEFF/, ''));
  if (!Array.isArray(plan) || !plan.length || plan.some(step =>
    !step || typeof step.tool !== 'string' || !step.tool ||
    (step.arguments !== undefined && (!step.arguments || typeof step.arguments !== 'object' ||
      Array.isArray(step.arguments))))) {
    throw new Error('The plan must be a nonempty array of {tool, arguments} objects');
  }

  const server = spawn(cli, ['mcp', '--headless', '--allow-path', job], {
    cwd: job,
    stdio: ['pipe', 'pipe', 'pipe'],
    windowsHide: true,
  });
  let pending;
  let nextId = 0;
  let error;
  let diagnostics = '';

  function fail(cause) {
    error ??= cause;
    if (pending) {
      clearTimeout(pending.timer);
      pending.reject(cause);
      pending = undefined;
    }
  }

  server.on('error', fail);
  server.on('exit', (code, signal) => fail(new Error('SolidCraft exited: ' + (signal || code))));
  server.stdin.on('error', fail);
  server.stderr.on('data', chunk => { diagnostics = (diagnostics + chunk).slice(-8000); });
  const lines = readline.createInterface({ input: server.stdout });
  lines.on('line', line => {
    let response;
    try {
      response = JSON.parse(line);
    } catch {
      fail(new Error('SolidCraft returned a non-JSON protocol line'));
      return;
    }
    if (!pending || response.id !== pending.id) return;
    const completed = pending;
    pending = undefined;
    clearTimeout(completed.timer);
    if (response.error) completed.reject(new Error(JSON.stringify(response.error)));
    else completed.resolve(response.result);
  });

  function call(method, params) {
    if (error) return Promise.reject(error);
    const id = ++nextId;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => fail(new Error('Timed out waiting for ' + method)), 60000);
      pending = { id, resolve, reject, timer };
      server.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n');
    });
  }

  try {
    const session = await call('initialize', {
      protocolVersion: '2025-06-18',
      capabilities: {},
      clientInfo: { name: 'cad-agent-workflow', version: '1.0.0' },
    });
    server.stdin.write('{"jsonrpc":"2.0","method":"notifications/initialized"}\n');
    const catalog = await call('tools/list', {});
    const available = new Set(catalog.tools.map(item => item.name));
    for (const step of plan) {
      if (!available.has(step.tool)) throw new Error('Unknown SolidCraft tool: ' + step.tool);
    }

    const results = [];
    for (const [index, step] of plan.entries()) {
      const result = await call('tools/call', {
        name: step.tool,
        arguments: step.arguments ?? {},
      });
      const items = result.content.map(item => {
        if (item.type !== 'text') return { type: item.type, mimeType: item.mimeType };
        try { return { type: item.type, data: JSON.parse(item.text) }; }
        catch { return { type: item.type, data: item.text }; }
      });
      if (result.isError) {
        throw new Error('Step ' + (index + 1) + ' (' + step.tool + '): ' + JSON.stringify(items));
      }
      results.push({ tool: step.tool, content: items });
    }
    console.log(JSON.stringify({ server: session.serverInfo, results }, null, 2));
  } catch (cause) {
    if (diagnostics) console.error(diagnostics.trim());
    throw cause;
  } finally {
    server.stdin.end();
    setTimeout(() => server.kill(), 2000).unref();
  }
}

run().catch(error => {
  console.error(error.message);
  process.exitCode = 1;
});