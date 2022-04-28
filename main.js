var fs = require('fs');

try {  
    var token = fs.readFileSync('TOKEN.txt', 'utf8');
} catch(e) {
    console.log('Error:', e.stack);
}

console.log(token.split("TOKEN=")[1].split('"')[1]);