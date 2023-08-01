var express = require('express');
var router = express.Router();

const multer = require('multer');
const upload = multer();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

// POST METHOD
router.post('/uploadImage', upload.any(), (req, res) => {
  console.log('\n\n\nreq\n\n\n');
  console.log(req)
  console.log('\n\n\nfile\n\n\n');
  console.log(req.files);

  res.status(200).send('uploaded');
})

module.exports = router;
