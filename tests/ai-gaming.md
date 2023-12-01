AI models can be trained on both perfect and imperfect information games, but the nature of the training process and the strategies involved may differ.

1. **Perfect Information Games:**
   - In perfect information games, all players have complete knowledge of the game state at all times. Examples include Chess, Checkers, and Go.
   - AI models for perfect information games often use techniques like Monte Carlo Tree Search (MCTS) combined with deep neural networks for evaluation.
   - Deep learning models, particularly convolutional neural networks (CNNs), have shown great success in learning complex patterns and strategies in perfect information games.

2. **Imperfect Information Games:**
   - In imperfect information games, players don't have full knowledge of the game state. Poker is a classic example where players have private information in the form of their own cards.
   - Training AI models for imperfect information games involves additional challenges. Reinforcement learning and game-theoretic approaches become crucial.
   - Techniques like Counterfactual Regret Minimization (CFR) are commonly used for training AI models in imperfect information games. CFR allows agents to learn strategies that converge to a Nash equilibrium.

3. **Hybrid Games:**
   - Some games have elements of both perfect and imperfect information. For example, games with hidden information or simultaneous move selection.
   - AI models for hybrid games need to adapt to both perfect and imperfect information aspects. This often involves a combination of techniques used in both types of games.

4. **Board Games vs. Video Games:**
   - AI models can be trained on various types of games, including traditional board games and modern video games.
   - For video games, reinforcement learning techniques are often applied. Deep Q-Networks (DQN) and Proximal Policy Optimization (PPO) are popular algorithms for training AI in video games.

In summary, the type of game influences the choice of techniques for training AI models. Whether a game is perfect or imperfect information, traditional or digital, determines the appropriate strategies and algorithms to employ in the training process. The field of AI game playing continues to evolve with ongoing research and the development of new methodologies.