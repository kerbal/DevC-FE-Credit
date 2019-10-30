const express = require('express');
const spawn = require('child_process').spawn;

const app = express();

app.get('/test', (req, res) => {
  const proc = spawn('python', ['./python/main.py', 'https://i.imgur.com/SS53U2m.png']);
  proc.stdout.on('data', (data) => {
    res.send(data.toString());
  });
});

app.listen(3000, async () => {
  console.log("Server is up");
});