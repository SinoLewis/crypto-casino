var Client = require('../lib/client'),
	Poker = require('../lib/poker'),
	Jinhua = require('../lib/jinhua_poker'),
	Holdem = require('../lib/holdem_poker');

import { io } from "socket.io-client";
var client = null;

Poker.toHTML = function (cards) {
	var html = '';
	for (var i = 0; i < cards.length; i++) {
		var card = cards[i];
		var color = card >> 4;
		var number = card & 0xf;
		var png = color + '_' + number + '.png';
		html += "<img src='img/" + png + "'/>";
	}
	return html;
};

// TODO: Exportable socket & client
var socket = io();

socket.log_traffic = true;
client = new Client(socket);

// TODO: Lang Inter & rm _T_ Jquery methods

// TODO: Use stores for Jquery DOM query 

// TODO: This Logic Block below goes to Root Svelte app from import socket & client
socket.on('hello', function (data) {
	$('#messages').empty();
	$('div#cmds').empty();
	showRoom(null);

	addMsg(data.msg);

	setTimeout(function () {
		var u = localStorage.getItem('x_userid');
		var p = localStorage.getItem('x_passwd');
		if (u && p) {
			login(u, p);
		} else {
			//socket.emit('hello', {});
			client.rpc('fastsignup', 0, parseSignUpReply);
		}
	}, 1000);
});

client.on('prompt', updateCmds);

client.on('shout', function (ret) {
	addMsg(ret.who.name + 'shout:' + ret.msg);
});
// TODO: This Logic Block Above goes to Root Svelte app

function parseSignUpReply(err, ret) {
	parseReply(err, ret);
	if (!err) {
		addMsg('account created:' + ret.uid + '/' + ret.passwd);
		login(ret.uid, ret.passwd);
	}
}

function onBtnClicked(e: Event) {
	var method = e.currentTarget.id;
	switch (method) {
		case 'fastsignup':
			client.rpc(method, e.currentTarget.getAttribute('arg'), parseSignUpReply);
			break;
		default:
			client.rpc(method, e.currentTarget.getAttribute('arg'), parseReply);
	}
}

function onInputBtnClicked(e) {
	var method = e.currentTarget.id;
	var el = document.querySelector('input#' + method)
	client.rpc(method, el.value, parseReply);
	el.value = '';
}

function onInputBoxEnter(e) {
	if (e.which == 13) onInputBtnClicked.call(this, e);
}


function login(u, p) {
	client.rpc('login', {
		uid: u,
		passwd: p
	}, function (err, ret) {
		if (err) {
			localStorage.removeItem('x_userid');
			localStorage.removeItem('x_passwd');
			echo(ret);
			socket.emit('hello', {});
		} else {
			var cmdsDiv = document.querySelector('div#cmds');
			var msgsDiv = document.querySelector('#messages');
			cmdsDiv.innerHTML = '';
			msgsDiv.innerHTML = '';
			showRoom(null);

			localStorage.setItem('x_userid', u);
			localStorage.setItem('x_passwd', p);
			addMsg(ret.token.uid + ' (' + ret.profile.name + ') ' + 'login success');

			if (ret.cmds) {
				updateCmds(ret.cmds);

				if ('entergame' in ret.cmds) {
					list_games();
				}
			}
		}

	});
}

function list_games() {
	client.rpc('games', 0, function (err, ret) {
		if (err) echo(ret);
		else {
			var roomnameElement = document.getElementById('roomname');
			roomnameElement.textContent = 'available games';
			var seatsUl = document.querySelector('#seats');
			seatsUl.innerHTML = '';

			for (var i = 0; i < ret.length; i++) {
				var game = ret[i];
				var str = (i + 1) + ', ' + game.id + ': ' + game.name + ' (' + game.desc + '), ' + game.rooms + ' rooms';
				var li = document.createElement('li');
				li.textContent = str;
				list.append(li);
			}
		}
	});
}

function list_rooms(gameid) {
	client.rpc('rooms', gameid, function (err, ret) {
		if (err) echo(ret);
		else {
			var roomnameElement = document.getElementById('roomname');
			roomnameElement.textContent = 'available games';
			var seatsUl = document.querySelector('#seats');
			seatsUl.innerHTML = '';
			for (var i = 0; i < ret.length; i++) {
				var room = ret[i];
				var str = 'room id: ' + room.id +
					', name: "' + room.name +
					'", seats: ' + room.seats_taken + '/' + room.seats_count +
					', gamers: ' + room.gamers_count;
				li.textContent = str;
				list.append(li);
			}
		}
	});
}

function addMsg(str) {
	var messagesUl = document.getElementById('messages');
	var li = document.createElement('li');
	li.textContent = str;
	li.classList.add('msg');
	messagesUl.appendChild(li);
	
	var msgElements = document.querySelectorAll('li.msg');
	var n = msgs.length - 20;
	if (n > 0) {
		for (var i = 0; i < n; i++) {
			messagesUl.splice(i, 1)
		}
	}
}