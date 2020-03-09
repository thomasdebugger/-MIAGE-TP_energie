// define remote server uri for matching in remote_server.js file
var fs = require('fs');

if (process.argv[2]) {
  fs.writeFile('scripts/remote_server.js', 'var tourServerUri = "' + process.argv[2] + '";', function (err) {
    if (err) throw err;
    console.log('Var replaced in remote_server.js!');
  });
}

