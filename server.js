var express = require('express'),
  app = express(),
  port = process.env.PORT || 3000;
    bodyParser = require('body-parser');



  app.use(bodyParser.urlencoded({ extended: true }));
  app.use(bodyParser.json());

app.use('/views', express.static(__dirname + '/views'));


  var routes = require('./routes/routes');
  routes(app);

app.listen(port);
