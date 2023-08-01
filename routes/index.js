var express = require('express');
var router = express.Router();

const multer = require('multer');
const upload = multer();

const { spawn } = require('child_process');

/* GET Method */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/chick', async (req, res) => {
  const change = () => {
    const yolo = `${process.cwd()}/public/pythons/best.pt`;
    const tflite = `${process.cwd()}/public/pythons/unet_quant.tflite`; 
    const result = spawn('python', [`${process.cwd()}/public/pythons/py.py`, `${process.cwd()}/public/images/kim.jpg`, yolo, tflite]);
    
    console.log(yolo)
    return new Promise((resolveFunc) => {
      result.stdout.on('data', (data) => {
        console.log(data.toString());
      });
      result.stderr.on('data', (data) => {
        console.log(`error: ${data.toString()}`);
      });
      result.on('exit', (code) => {
        resolveFunc(code)
      });
    });
  }
  await change();

  res.render('index', { title: 'hello' });
})

/* POST Method */
router.post('/uploadImage', upload.any(), (req, res) => {
  const { files } = req;

  res.status(200).send('uploaded');
})

module.exports = router;
