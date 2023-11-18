import gymnasium as gym

gym.register(
    id='Game2048-v0',
    entry_point='gymcustomenv:Env2048',
    kwargs={}
)