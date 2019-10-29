const WebSocket = require('ws');
const shelljs = require('shelljs');

const execCmd = content => {
    const cmd = "python3 ./ai-text-processor/main.py '" + content.replace(/[']/g, '\\') + "'";
    return shelljs.exec(cmd, {silent: false}).stdout;
};

const wss = new WebSocket.Server({ port: 5000, host: '0.0.0.0' });

wss.on('connection', ws => {
  ws.on('message', data => {
    const msg = JSON.parse(data);
    ws.send("This is what I derived: " + execCmd(msg.message));
  });
});
