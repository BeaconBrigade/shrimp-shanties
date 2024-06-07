# `shrimp-shanties`

Shrimp shanties is a rhythm game where you try to catch shrimp falling into the water
on the time of the beat. There are multiple songs you can play to have a unique experience
after you master each song.

## Credits

Project completed by Colton, Sean and Ryan.

## Pseudo Code

A very simplified model of the code base that doesn't follow perfectly the way the game
runs.

```python
load_pygame()

menu = set_state(Menu)

while not menu.closed():
    pass

connect = set_state(ConnectScreen)

shanty_title = select_shanty(connect)

game = load_game(shanty_title)

while game.is_playing():
    events = process_pygame_events()
    pass_events_to_entities(events)
    update_entity_state()
    
    draw_screen()

    if game.paused():
        if game.pause.exit_game():
            # go back to menu
            set_state(ConnectScreen)
    if game.over():
        set_state(GameOver)
        break

show_post_game_stats()

unload_pygame()
```

## Programming Model

The program has three main concepts: [`State`](shrimp_shanties/state.py),
[`Entity`](shrimp_shanties/game/entity/__init__.py) and [`Check`](shrimp_shanties/game/check/__init__.py).
Each are used to help dictate how events are passed throughout the game and pieces of code can interact
with each other.

### Events

`shrimp-shanties` uses the `pygame` events system (`pygame.event`) to pass messages around
the code. When a user presses a key, `pygame` emits a `KEYDOWN` event which the program can
listen for. When a game event occurs, such as a `Note` in a shanty being missed, a custom
event is emitted so that score keeping entities or the `Note` itself know to despawn.
Entities and `State` listen for different events to know when to update themselves or interact
with other `State` or entities.

### [`State`](shrimp_shanties/state.py)

States are the overarching loop of what the game is doing. States work like a stack, where,
as the game progresses different states are pushed and popped onto the stack. The top state
is the one that is currently running. 

Each State has a `draw`, `update` and `handle_event` method to override. `draw` renders the 
current view to the screen. `update` is called each frame to run code to update game state
every frame. `handle_event` is a way to process all the events described in the above section.

Let's look at an example: the `Connection` state (found [here](shrimp_shanties/menu/connection.py)). 
This is the screen where users select which shanty they want to play, choose whether to play 
online/offline or can visit the marketplace. In the `Connection.__init__` function the ui elements
are instantiated and appended to the special `State.ui_elements` variable which is a feature of the
`State` class. This ensures ui elements are automatically shown/hidden when different are on the top
of the stack or not. The `draw` method simply draws a background colour because 
[`pygame_gui`](https://pygame-gui.readthedocs.io/en/latest/) automatically draws ui elements in
[shrimp_shanties/\_\_init\_\_.py](shrimp_shanties/__init__.py). Next is the `handle_event` function
which you can see has several events to it checks for. The first event it checks for is if the
button which says "Online" is pressed. If that button is pressed it then starts the game by pushing
the [Game](shrimp_shanties/game/__init__.py) state with the user-selected shanty.

### [`Entity`](shrimp_shanties/game/entity/__init__.py)

Entities are a part of the gameplay in `shrimp-shanties`. They are objects that also have interactions
between each other every frame. Entities are spawned in and registered to the
[EntityManager](shrimp_shanties/game/entity_manager.py). The entity manager takes events passed from the
[Game](shrimp_shanties/game/__init__.py) state and passes them onto entities that require those events.
When an entity is spawned it registers with the event manager which events it would like to receive,
and the entity manager will pass those along. Each entity is automatically registered for the
[PROCESS_TURN](shrimp_shanties/game/entity_manager.py) event which means each frame each entity will
get a chance to update its state. For example, the [Note](shrimp_shanties/game/rhythm/note.py) entity
will slowly move itself down the screen. Entities also have their own draw method which is called each
frame by the entity manager. Entities draw themselves in their correct position onto the screen. Not
all entities are visible however, such as the [NoteSpawner](shrimp_shanties/game/rhythm/note_spawner.py)
entity which is responsible for creating notes on the right beat.

### [`Check`](shrimp_shanties/game/check/__init__.py)

Checks are essentially functions that are run in the game to generate events. There are two kinds:
[ActiveCheck](shrimp_shanties/game/check/__init__.py) and [PassiveCheck](shrimp_shanties/game/check/__init__.py).
Passive checks are run every frame with access to the entity manager and can generate an event which will
be passed to entities who want to hear it. Active checks, similar to entities, listen for specific events,
which the enity manager will pass to them. An active check can also generate events which are then forwarded
to listening entities. An example of an active check is [InputTiming](shrimp_shanties/game/check/input_timing.py).
`InputTiming` listens for user key presses and then will do collision checks between notes and the judgement
line. If the input is a success, it will generate despawn the note and send an event to update the score.

## Creating your own shanties

Shanties can be created both manually and generated automatically. For information on building a shanty
manually, look [here](assets/shanties/README.md). For generating shanties we will be using
[shanty-gen.py](scripts/shanty-gen.py). You can run `shanty-gen.py` from any directory using python. You
also aren't required to be in the virtual environment. `shanty-gen.py` randomly generates a shanty with a
given name and optionally given music/video/backgrounds. You can specify multiple parameters about the
generated shanty. Try running `python shanty-gen.py -h` to see more information.

## Installation: Development

```bash
# clone the code
git clone https://github.com/beaconbrigade/shrimp-shanties.git
cd shrimp-shanties

# set up python virtual environment
python -m venv venv
# on windows run:
./venv/Scripts/activate
# on macos or linux run:
./venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

## Running: Development

It does not matter what directory you run `main.py` from, it will find the game and assets folders.

```bash
# in the virtual environment:
python main.py
```
