var express = require('express');
var router = express.Router();
var path = require('path');

/* GET home page. */
/*
router.get('/', function(req, res, next) {
	res.render('index', { title: 'Express' });
});
*/
/* GET settings page */
/*
router.get('/settings', function(req, res, next) {
	res.render('settings');
});
*/

/* GET React App */
//router.get(['dashboard', '/app', '/app/*'], function(req, res, next) {
router.get(['/app/*'], function(req, res, next) {
	res.sendFile(path.join(__dirname, '../public', 'index.html'));
});

module.exports = router;
