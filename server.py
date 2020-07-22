import asyncio
import json
from random import randint
from game import Game
from deck import AllCards

all = AllCards()


async def handle_client(reader, writer):
    request = None
    while request != 'quit':
        # try:
            print('REQ', request)
            request = (await reader.read(255)).decode('utf8')
            if request is None:
                writer.write(json.dumps({'id': 'x', 'error': 'No data!'}).encode('utf8'))
                await writer.drain()
                continue
            try:
                if request is not None:
                    data = json.loads(request)
                else:
                    data = {'id': 'x', 'error': 'Empty request!'}
            except json.JSONDecodeError:
                writer.write(json.dumps({'id': 'x', 'error': 'Bad data!'}).encode('utf8'))
                await writer.drain()
                continue
            player_id = data.get('id')
            # print(player_id)
            if player_id not in [player.name for player in game.players]:
                writer.write(json.dumps({'id': player_id, 'error': 'No player with with name!'}))
                await writer.drain()
                continue

            player = game.get_player(player_id)
            message_type = data.get('type')
            if message_type == 'sync':
                response = {'id': player_id, 'type': 'sync',
                            'update': player.update_available,
                            'players_ready': game.get_ready_players(), 'move_ready': player.move_available,
                            'queue': 0,
                            'player_waiting': True if player.ready_to_built is not None else False,
                            'left_waiting': True if player.left_neighbor.ready_to_built is not None else False,
                            'right_waiting': True if player.right_neighbor.ready_to_built is not None else False}
            elif message_type == 'get_data':
                response = {'id': player_id, 'type': 'get_data',
                            'state': player.state,
                            'cards': [card.id for card in player.available_cards],
                            'wonder': player.wonder.id,
                            'left_neighbor': [player.left_neighbor.wonder.id, len(player.left_neighbor.available_cards), player.left_neighbor.state],
                            'right_neighbor': [player.right_neighbor.wonder.id, len(player.right_neighbor.available_cards), player.right_neighbor.state],
                            'vp': player.total_vp,
                            'money': game.get_player_neighbor_money(player), 'military': game.get_player_neighbor_military(player),
                            'wins': game.get_player_neighbor_wins(player), 'loses': game.get_player_neighbor_loses(player),
                            'age': game.age, 'round': game.round}
                player.update_available = False
            elif message_type == 'first_get_data':
                response = {'id': player_id, 'type': 'first_get_data',
                            'state': player.state,
                            'cards': [card.id for card in player.available_cards],
                            'built_cards': [card.id for card in player.built_cards],
                            'left_built_cards': [card.id for card in player.left_neighbor.built_cards],
                            'right_built_cards': [card.id for card in player.right_neighbor.built_cards],
                            'wonder': player.wonder.id,
                            'left_neighbor': [player.left_neighbor.wonder.id, len(player.left_neighbor.available_cards),
                                              player.left_neighbor.state],
                            'right_neighbor': [player.right_neighbor.wonder.id, len(player.right_neighbor.available_cards),
                                               player.right_neighbor.state],
                            'vp': player.total_vp,
                            'money': game.get_player_neighbor_money(player),
                            'military': game.get_player_neighbor_military(player),
                            'wins': game.get_player_neighbor_wins(player), 'loses': game.get_player_neighbor_loses(player),
                            'age': game.age, 'round': game.round}
                player.update_available = False
            elif message_type == 'get_move':
                response = {'id': player_id, 'type': 'get_move',
                            'player_built': player.last_built,
                            'left_neighbor_built': player.left_neighbor.last_built,
                            'right_neighbor_built': player.right_neighbor.last_built,
                            'player_money_delta': player.delta}
                player.move_available = False
                game.update_emitted_move(player)
            elif message_type == 'build':
                if player.state != 1:
                    success = True
                    player.state = 1
                    building = data.get('building')
                    chosen = data.get('chosen')
                    discard = data.get('discard')
                    game.prepare_for_build(player, building, chosen, discard)
                else:
                    success = True

                response = {'id': player_id, 'type': 'build', 'status': success}
                if game.get_ready_players() == 3:
                    game.build()
                    game.move_ready()
            elif message_type == 'card_details':
                if 'card_id' not in data.keys():
                    response = {'id': player_id, 'error': 'Invalid message'}
                else:
                    card_id = data.get('card_id')

                    response = {'id': player_id, 'type': 'card_details',
                                'resources_needed': all.get_card_cost(card_id),
                                'resources_available': game.check_player_resources(player, card_id),
                                'upgrade': game.check_upgrade(player, card_id),
                                'status': game.get_card_status(card_id)}
            elif message_type == 'wonder_details':
                wonder_id = data.get('wonder_id')

                response = {'id': player_id, 'type': 'wonder_details',
                            'stage': player.built_wonders,
                            'resources_needed': player.get_next_wonder_cost(),
                            'resources_available': game.check_player_resources(player, 0, wonder=True)}
            else:
                response = {'id': player_id, 'error': 'Invalid message'}

            # if message_type != 'sync':
            print("RES", response)
            writer.write(json.dumps(response).encode('utf8'))
            await writer.drain()
        # except:
        #     print("Error")
    writer.close()

loop = asyncio.get_event_loop()
game = Game()

loop.create_task(asyncio.start_server(handle_client, 'localhost', 15555))
loop.run_forever()
