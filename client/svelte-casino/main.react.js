
var Client = require('../lib/client'),
	Poker = require('../lib/poker'),
	Jinhua = require('../lib/jinhua_poker'),
	Holdem = require('../lib/holdem_poker');

import { io } from "socket.io-client";
var client = null;

Poker.toHTML = function(cards) {
	var html = '';
	for(var i=0; i<cards.length; i++) {
		var card = cards[i];
		var color = card >> 4;
		var number = card & 0xf;
		var png = color + '_' + number + '.png';
		html += "<img src='img/" + png + "'/>";
	}
	return html;
};

var socket = io();
	
socket.log_traffic = true;

client = new Client(socket);

// TODO: Lang Inter & rm _T_ Jquery methods

// TODO: Use stores for Jquery DOM query 
const [messages, setMessages] = useState(null);
const [divCmds, setDivCmds] = useState(null);

socket.on('hello', function(data){
    // $('#messages').empty();
    // $('div#cmds').empty();
    setMessages(null)
    setDivCmds(null)
    showRoom(null);
    
    addMsg(data.msg);
    
    setTimeout(function(){
        var u = localStorage.getItem('x_userid');
        var p = localStorage.getItem('x_passwd');
        if(u && p) {
            login(u, p);
        } else {
            //socket.emit('hello', {});
            client.rpc('fastsignup', 0, parseSignUpReply);
        }
    }, 1000);
});

client.on('prompt', updateCmds);

client.on('shout', function(ret){
    addMsg(ret.who.name + 'shout:' + ret.msg);
});


function parseSignUpReply(err,ret){
	parseReply(err,ret);
	if(! err) {
		addMsg('account created:' + ret.uid + '/' + ret.passwd);
		login(ret.uid, ret.passwd);
	}
}

function onBtnClicked(e) {
	var method = $(this).attr('id');
	switch(method) {
	case 'fastsignup':
		client.rpc(method, $(this).attr('arg'), parseSignUpReply);
		break;
	default:
		client.rpc(method, $(this).attr('arg'), parseReply);
	}
}