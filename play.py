import asyncio
import random
import os
import json
from dotenv import load_dotenv
from ah2ac2.evaluation.evaluation_space import EvaluationSpace
from ah2ac2.evaluation.evaluation_environment import EvaluationEnvironment
from agents.agent import Agent
from agents.random_agent import RandomAgent

load_dotenv()

_TEST_API_KEY = os.getenv("TEST_API_KEY")

with open("action_descriptions.json", "r") as f:
    ACTION_DESCRIPTIONS = json.load(f)


async def play_game(env: EvaluationEnvironment, agent: Agent, history_file: str = None):
    """
    Plays a single game of Hanabi using the inputted controlled agent and optionally saves all moves to a history file,
    if specified.

    Args:
        env: The evaluation environment to play the game in.
        agent: The controlled agent that will play the game with human proxies.
        history_file: The path to the file to save the game history to.

    Raises:
        Exception: If an error occurs during the game.

    Authors:
        - AH2AC2 Team: ah2ac2@proton.me
        - Hanabi Evaluation Subgroup at the University of Toronto (repository authors).
    """
    try:
        # Get a clean set of initial observations and legal moves
        observations, legal_moves = await env.reset()
        print(legal_moves)
        print(f"Game started. ID: {env.info.game_id}, Controlling: {env.info.candidate_controlling}")

        if history_file:
            with open(history_file, "w") as f:
                f.write(f"Game ID: {env.info.game_id}\n")
                f.write(f"Controlling: {env.info.candidate_controlling}\n")

        # Assign agent to the role defined in env.info.candidate_controlling
        my_agent = {env.info.candidate_controlling[0]: agent}

        done = False
        current_score = 0.0

        while not done:
            actions_to_send = {}
            for agent_id in env.info.candidate_controlling:
                obs_for_agent = observations[agent_id]
                legal_moves_for_agent = legal_moves[agent_id]

                # Get action from our specific agent instance
                action, my_agent[agent_id] = my_agent[agent_id].act(obs_for_agent, legal_moves_for_agent)
                actions_to_send[agent_id] = action

                if history_file:
                    with open(history_file, "a") as f:
                        f.write(f"Agent {agent_id} took action: {action} ({ACTION_DESCRIPTIONS[action - 1]})\n")

            # Send actions and get the next state
            observations, current_score, done, legal_moves = await env.step(actions_to_send)
            print(f"Step taken. Score: {current_score}, Done: {done}")

        print(f"Game ID {env.info.game_id} finished. Final score: {current_score}")
        if history_file:
            with open(history_file, "a") as f:
                f.write(f"Final score: {current_score}\n")

    except Exception as e:
        print(f"Error during game {env.info.game_id if env._info else 'Unknown'}: {e}")

if __name__ == "__main__":
    # Initialize a test evaluation space
    eval_space_test = EvaluationSpace(_TEST_API_KEY)

    # Randomly determine a play position for our controlled agent
    agent_positions = [0, 1, 2]
    agent_position = random.choice(agent_positions)

    # Create a three-player test environment with the specified agent position
    test_env_3p: EvaluationEnvironment = eval_space_test.new_test_environment(
        num_players=3,
        candidate_position=[agent_position]
    )

    # Create the agent we are controlling: by default, it will be one RandomAgent.
    agent_to_play = RandomAgent()

    # Define the history file path
    history_file_path = os.path.join("game_logs", "game_history.txt")

    # Play the game!
    asyncio.run(play_game(test_env_3p, agent_to_play, history_file_path))