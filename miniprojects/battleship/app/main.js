// GAME SETUP
var initialState = SKIPSETUP ? "playing" : "setup";
var gameState = new GameState({state: initialState});
var cpuBoard = new Board({autoDeploy: true, name: "cpu"});
var playerBoard = new Board({autoDeploy: SKIPSETUP, name: "player"});
var cursor = new Cursor();

// UI SETUP
setupUserInterface();

// selectedTile: The tile that the player is currently hovering above
var selectedTile = false;

// grabbedShip/Offset: The ship and offset if player is currently manipulating a ship
var grabbedShip = false;
var grabbedOffset = [0, 0];

// isGrabbing: Is the player's hand currently in a grabbing pose
var isGrabbing = false;

// MAIN GAME LOOP
// Called every time the Leap provides a new frame of data
Leap.loop({ hand: function(hand) {
  // Clear any highlighting at the beginning of the loop
  unhighlightTiles();

  // TODO: 4.1, Moving the cursor with Leap data
  // Use the hand data to control the cursor's screen position
  var offsetDown = 400;
  var left = hand.screenPosition()[0];
  var bottom = hand.screenPosition()[1]+offsetDown;
  var cursorPosition = [left,bottom];

  //var cursorPosition = [left,bottom];
  //console.log(cursorPosition[0]);
  cursor.setScreenPosition(cursorPosition);

  // TODO: 4.1
  // Get the tile that the player is currently selecting, and highlight it
  //selectedTile = ?

  selectedTile = getIntersectingTile(cursorPosition);
  var color = Colors.RED;
  if(!(selectedTile==false)){
    //position: {row: cursorPosition[0], col: cursorPosition[1]};
    highlightTile(selectedTile, color);
    //console.log(cursorPosition);
  }

  // SETUP mode
  if (gameState.get('state') == 'setup') {
    background.setContent("<h1>battleship</h1><h3 style='color: #7CD3A2;'>deploy ships</h3>");
    // TODO: 4.2, Deploying ships
    //  Enable the player to grab, move, rotate, and drop ships to deploy them

    //////////////////
    var hover=false;
    if(!isGrabbing){
    hover = getIntersectingShipAndOffset(cursorPosition);
  }
    if(hover!=false){
    ship = hover.ship;
    shipOffset  = hover.offset;
  }

    //////////////////




    // First, determine if grabbing pose or not

    isGrabbing = (hand.grabStrength>=.85);

    // Grabbing, but no selected ship yet. Look for one.
    // Update grabbedShip/grabbedOffset if the user is hovering over a ship
    if (!grabbedShip && isGrabbing) {
      grabbedShip=true;
    }

    // Has selected a ship and is still holding it
    else if (grabbedShip && isGrabbing) {
      ship.setScreenPosition([left-shipOffset[0],bottom-shipOffset[1]]);
      ship.setScreenRotation(-hand.roll());
    }

    // Finished moving a ship. Release it, and try placing it.
    // TODO: Try placing the ship on the board and release the ship
    else if (grabbedShip && !isGrabbing) {
      placeShip(ship);
      grabbedShip=false;
    }
  }

  // PLAYING or END GAME so draw the board and ships (if player's board)
  // Note: Don't have to touch this code
  else {
    if (gameState.get('state') == 'playing') {
      background.setContent("<h1>battleship</h1><h3 style='color: #7CD3A2;'>game on</h3>");
      turnFeedback.setContent(gameState.getTurnHTML());
    }
    else if (gameState.get('state') == 'end') {
      var endLabel = gameState.get('winner') == 'player' ? 'you won!' : 'game over';
      background.setContent("<h1>battleship</h1><h3 style='color: #7CD3A2;'>"+endLabel+"</h3>");
      turnFeedback.setContent("");
    }

    var board = gameState.get('turn') == 'player' ? cpuBoard : playerBoard;
    // Render past shots
    board.get('shots').forEach(function(shot) {
      var position = shot.get('position');
      var tileColor = shot.get('isHit') ? Colors.RED : Colors.YELLOW;
      highlightTile(position, tileColor);
    });

    // Render the ships
    playerBoard.get('ships').forEach(function(ship) {
      if (gameState.get('turn') == 'cpu') {
        var position = ship.get('position');
        var screenPosition = gridOrigin.slice(0);
        screenPosition[0] += position.col * TILESIZE;
        screenPosition[1] += position.row * TILESIZE;
        ship.setScreenPosition(screenPosition);
        if (ship.get('isVertical'))
          ship.setScreenRotation(Math.PI/2);
      } else {
        ship.setScreenPosition([-500, -500]);
      }
    });

    // If playing and CPU's turn, generate a shot
    if (gameState.get('state') == 'playing' && gameState.isCpuTurn() && !gameState.get('waiting')) {
      gameState.set('waiting', true);
      generateCpuShot();
    }
  }
}}).use('screenPosition', {scale: LEAPSCALE});

// processSpeech(transcript)
//  Is called anytime speech is recognized by the Web Speech API
// Input:
//    transcript, a string of possibly multiple words that were recognized
// Output:
//    processed, a boolean indicating whether the system reacted to the speech or not
var processSpeech = function(transcript) {
  // Helper function to detect if any commands appear in a string
  var userSaid = function(str, commands) {
    for (var i = 0; i < commands.length; i++) {
      if (str.indexOf(commands[i]) > -1)
        return true;
    }
    return false;
  };

  var processed = false;
  if (gameState.get('state') == 'setup') {
    // TODO: 4.3, Starting the game with speech
    // Detect the 'start' command, and start the game if it was said
    var start = userSaid(transcript,['start']);
    
    if (start) {
      spch  = "Welcome to battleship! Just to warn you, you could quickly go down the drain.";
      generateSpeech(spch);
      spch  = "To setup, please place your ship on the board by grabbing, dragging and dropping! When you're happy with your placement, please say START!";
      generateSpeech(spch);
      spch  = "Keep in mind, if you don't place your ship, it will be on my ship and I will destroy you early!";
      generateSpeech(spch);
      spch  = "To go back to the setup, please refresh the page!";
      generateSpeech(spch);
      spch  = "when you're ready to go, point to the tile you wish to fire on, and clearly say fire";
      generateSpeech(spch);
     

      gameState.startGame();
      processed = true;
    }
  }
  
  else if (gameState.get('state') == 'playing') {
    if (gameState.isPlayerTurn()) {
      // 4.4, Player's turn
      // Detect the 'fire' command, and register the shot if it was said

      var fire = userSaid(transcript,['fire']);
      if (fire) {
        registerPlayerShot();

        processed = true;
      }
    }

    else if (gameState.isCpuTurn() && gameState.waitingForPlayer()) {
      //4.5, CPU's turn
      // Detect the player's response to the CPU's shot: hit, miss, you sunk my ..., game over
      // and register the CPU's shot if it was said
      p_response = userSaid(transcript.toLowerCase(),['hit','miss','you sunk my ship','game over']);
      if (p_response) {
        var response = transcript;
        registerCpuShot(response);

        processed = true;
      }
    }
  }

  return processed;
};

// TODO: 4.4, Player's turn
// Generate CPU speech feedback when player takes a shot
var registerPlayerShot = function() {
  // TODO: CPU should respond if the shot was off-board
  if (!selectedTile) {
    generateSpeech("Not a tile! HAHAHAHAHAHAH! LOOOL!");
  }
  // If aiming at a tile, register the player's shot
  else {
    console.log('selected the title');
    var shot = new Shot({position: selectedTile});
    var result = cpuBoard.fireShot(shot);

    // Duplicate shot
    if (!result) return;

    // TODO: Generate CPU feedback in three cases
    // Game over
    if (result.isGameOver) {
      var words = ["Bye Bye!", "See you later!", "Go home!", "Nice game!"];
        var item = words[Math.floor(Math.random()*words.length)];
      generateSpeech("Game over! "+item);
      gameState.endGame("player");
      return;
    }
    // Sunk ship
    else if (result.sunkShip) {
      generateSpeech("I lost a ship! Who cares! Monsters don't need weapons to survive!");
      var shipName = result.sunkShip.get('type');
    }
    // Hit or miss
    else {
      var isHit = result.shot.get('isHit');
      if(isHit){
        var words = ["You're mean!", "Surprised!", "Wow!", "I am scared!"];
        var item = words[Math.floor(Math.random()*words.length)];
        generateSpeech("ouch! "+item);
      }
      else{
        var words = ["Not surprised!","You're not multimodal enough!", "Remember, this is a coordination game!", "Nice try!", "You're wasting my time!","HAHAHAHA!"];
        var item = words[Math.floor(Math.random()*words.length)];
        generateSpeech("Miss! "+item);
      }
    }

    if (!result.isGameOver) {
      // TODO: Uncomment nextTurn to move onto the CPU's turn
      nextTurn();
    }
  }
};

// TODO: 4.5, CPU's turn
// Generate CPU shot as speech and blinking
var cpuShot;
var generateCpuShot = function() {
  // Generate a random CPU shot
  cpuShot = gameState.getCpuShot();
  var tile = cpuShot.get('position');
  var rowName = ROWNAMES[tile.row]; // e.g. "A"
  var colName = COLNAMES[tile.col]; // e.g. "5"
  generateSpeech("Fire at "+rowName+colName+'!');
  blinkTile(tile);

  // TODO: Generate speech and visual cues for CPU shot
};

// TODO: 4.5, CPU's turn
// Generate CPU speech in response to the player's response
// E.g. CPU takes shot, then player responds with "hit" ==> CPU could then say "AWESOME!"
var registerCpuShot = function(playerResponse) {
  // Cancel any blinking
  unblinkTiles();
  var result = playerBoard.fireShot(cpuShot);

  // NOTE: Here we are using the actual result of the shot, rather than the player's response
  // In 4.6, you may experiment with the CPU's response when the player is not being truthful!
  var isTrueFul = function(expected){
    var match = false;
    var resp = playerResponse.toLowerCase();
    if (!resp.includes(expected)){
      var words = ["Please go see an eye doctor!", "Stop lying!", "Nice try loser!", "Open your eyes!"];
      var item = words[Math.floor(Math.random()*words.length)];
      var speech  = "This is not a "+playerResponse+". This is a "+expected+". "+item;
      generateSpeech(speech);
    }

  }

  // TODO: Generate CPU feedback in three cases
  // Game over
  var expected = "hit";
  if (result.isGameOver) {
    expected = "game over";
    isTrueFul(expected);
    generateSpeech("See you later loser!");
    gameState.endGame("cpu");
    return;
  }
  // Sunk ship
  else if (result.sunkShip) {
    expected="sunk";
    isTrueFul(expected);
    generateSpeech('Rest in Piece!');
    var shipName = result.sunkShip.get('type');
  }
  // Hit or miss
  else {
    var isHit = result.shot.get('isHit');
    if (isHit){
      isTrueFul(expected);
      var words = ["Got it!","Not surprised!", "Routine!", "All day!", "You're going down!","Like the ranger do!"];
      var item = words[Math.floor(Math.random()*words.length)];
      generateSpeech('Yay!Yay! '+item);
    }
    else{
      expected = "miss";
      isTrueFul(expected);
      var words = ["Next time!","You got lucky!", "I am going easy on you!", "I miss fired!", "You must be releived!","I can't believe it!"];
      var item = words[Math.floor(Math.random()*words.length)];
      generateSpeech(item);
    }
  }

  if (!result.isGameOver) {
    // nextTurn to move onto the player's next turn
    nextTurn();
  }
};

