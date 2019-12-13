var express = require('express');
var router = express.Router();

/* GET users listing. */

/*
This means /api/
*/
router.get('/', function(req, res, next) {
	res.json(['A', 'B', 'C']);
});

/*
This means /api/getServices
*/
router.get('/getServices', function(req, res, next) {
	res.json(['servA', 'servB', 'servC']);
});

module.exports = router;
