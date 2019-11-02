const express = require('express');
const spawn = require('child_process').spawn;
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json())

app.post('/test', async (req, res) => {
  try {
    const { IDCardImageURL, SelfieImageURL, Form } = req.body;
    const proc = spawn('python', ['./python/main.py', IDCardImageURL, SelfieImageURL, Form]);
    proc.stdout.on('data', (data) => {
      res.send({response: data.toString()});
    });
  }
  catch (error) {
    res.status(400).send(error.message);
  }
});

app.listen(3000, async () => {
  console.log("Server is up");
});