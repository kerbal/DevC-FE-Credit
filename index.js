const express = require('express');
const spawn = require('child_process').spawn;

const app = express();

app.get('/sum', (req, res) => {
  // http://localhost:3000/sum?a=5&b=7
  
  const { a, b } = req.query;
  const proc = spawn('python', ['./python/main.py', a, b]);

  proc.stdout.on('data', (data) => {
    res.send(data.toString());
  });
});

app.listen(3000, () => {
  console.log("Server is up");
});