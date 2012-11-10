var leftVoteButton;
var rightVoteButton;
var nameField;
var messageField;
var channel;
var hasBroadcastedJoined = false;
var lastInsertedMessageTime = new Date(0);

$(document).ready(function() {
  leftVoteButton = $("#left-vote-button");
  rightVoteButton = $("#right-vote-button");
  leftVoteButton.click(leftVoteButtonClicked);
  rightVoteButton.click(rightVoteButtonClicked);

  nameField = $(".chat-input-name");
  messageField = $(".chat-input");
  nameField.keypress(onNameChanged);
  nameField.blur(onNameChanged);
  messageField.keypress(onMessageChanged);
  messageField.attr("disabled", "true");
  messageField.attr("placeholder", "Enter a name to continue");

  channel = connect();

  $('i').each(function(idx) {
    if($(this).data('css') != null)
      document.styleSheets[1].insertRule('.'  + $(this).data('css') + ':after { content: "' + $(this).data('title').replace(/-/g, ' ') + '"; }', 0);
  })

});

$(window).load(function() {
  // horizontally center landscape pictures
  // $(".cbimg").each(function(i) { if($(this).width() > $(this).height()) { $(this).css('margin-top', (432 - parseInt($(".cbimg:eq(1)").css('height')))/3 + 'px') } });

})

function connect() {
  var client = {
    connect: onConnect,
    event_queue: onMessage
  };
  return new IMO.Channel(client);
}

function onConnect() {
  channel.subscribe([{"type": "event_queue", "name": "redditmash"}], 0);
}

function onMessage(name, event) {
  var messageTime = new Date(0);
  messageTime.setUTCSeconds(event.timestamp);
  if(messageTime.getMinutes() != lastInsertedMessageTime.getMinutes()) {
    insertTimeMessage(messageTime.toLocaleTimeString());
  }
  lastInsertedMessageTime = messageTime;
  insertChatMessage(event.object.message);
}

function onNameChanged(event) {
  if(!hasBroadcastedJoined && nameField.val() != "" && (event.keyCode == 13 || event.type == "blur")) {
    hasBroadcastedJoined = true;
    channel.event_queue(
      "redditmash",
      {"object": {"message": nameField.val() + " joined the chat."}}
    );
  }
  if(nameField.val() == "") {
    messageField.attr("disabled", "");
    messageField.attr("placeholder", "Enter a name to continue");
  } else
  {
    messageField.removeAttr("disabled");
    messageField.attr("placeholder", "Message");
  }
  if(event.keyCode == 13) {
    return false;
  }
}

function onMessageChanged(event) {
  if(messageField.val() != "" && event.keyCode == 13) {
    channel.event_queue(
      "redditmash",
      {"object": {"message": nameField.val() + ": " + messageField.val()}}
    );
    messageField.val("");
    return false;
  }

  return event.keyCode != 13;
}

function insertChatMessage(message) {
  $('.chat-table > tbody:last').append('<tr><td>' + message + '</td></tr>');
  $(".chat-div:eq(0)").scrollTop(999999);
}

function insertTimeMessage(message) {
  $('.chat-table > tbody:last').append('<tr><td class="chat-time-message">' + message + '</td></tr>');
  $(".chat-div:eq(0)").scrollTop(999999);
}


function leftVoteButtonClicked() {
  return false;
}

function rightVoteButtonClicked() {
  return false;
}

String.prototype.toHHMMSS = function () {
    sec_numb    = parseInt(this);
    var hours   = Math.floor(sec_numb / 3600);
    var minutes = Math.floor((sec_numb - (hours * 3600)) / 60);
    var seconds = sec_numb - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    var time    = hours+':'+minutes+':'+seconds;
    return time;
}
