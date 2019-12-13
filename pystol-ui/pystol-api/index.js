var express = require('express');
var router = express.Router();
var path = require('path');

/* GET React App */
router.get(['/app/*'], function(req, res, next) {
	res.sendFile(path.join(__dirname, '../public', 'index.html'));
});

module.exports = router;
