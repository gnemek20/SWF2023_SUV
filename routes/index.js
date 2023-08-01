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
  const { file } = req;
  console.log('\n\n\n req \n\n\n');
  console.log(req);
  console.log('\n\n\n body \n\n\n');
  console.log(req.body)
  console.log(file);

  res.status(200).send();
})

module.exports = router;
