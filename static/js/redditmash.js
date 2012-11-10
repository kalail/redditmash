var leftVoteButton;
var rightVoteButton;
var nameField;
var messageField;
var channel;
var hasBroadcastedJoined = false;

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
}

function leftVoteButtonClicked() {
  return false;
}

function rightVoteButtonClicked() {
  return false;
}
