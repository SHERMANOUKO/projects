var express = require('express'),
    app = express(),
    port = process.env.PORT || 3000,
    mongoose = require('mongoose')
    Task = require('./api/models/todoListModels'),
    bodyParser = require('body-parser');

//mongoose instance connection url connection
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost/Tododb');

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

//import routes
var routes = require('./api/routes/todoListRoutes');

//register routes
routes(app)

//middleware for wroung route access
app.use(function(req, res) {
    res.status(404).send({url: req.originalUrl + ' not found'})
});

app.listen(port, () =>{
    console.log("App has started on port "+ port)
})
