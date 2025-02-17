import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

class LorenzChaosAnimation:
    def __init__(self, sigma=10, rho=28, beta=8/3):
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
    
    def lorenz(self, t, state):
        """Lorenz system equations"""
        x, y, z = state
        dx = self.sigma * (y - x)
        dy = x * (self.rho - z) - y
        dz = x * y - self.beta * z
        return [dx, dy, dz]
    
    def generate_initial_conditions(self, n_trajectories=100, noise_scale=0.1):
        """Generate slightly different initial conditions around a point"""
        base_state = np.array([1.0, 1.0, 1.0])
        
        # Generate random perturbations
        perturbations = noise_scale * np.random.randn(n_trajectories, 3)
        
        # Add perturbations to base state
        initial_conditions = base_state + perturbations
        
        return initial_conditions
    
    def simulate_trajectories(self, t_span, dt, initial_conditions):
        """Simulate multiple trajectories"""
        t = np.arange(t_span[0], t_span[1], dt)
        n_trajectories = len(initial_conditions)
        
        # Array to store all trajectories
        trajectories = np.zeros((n_trajectories, len(t), 3))
        
        # Simulate each trajectory
        for i in range(n_trajectories):
            sol = solve_ivp(
                self.lorenz,
                t_span,
                initial_conditions[i],
                t_eval=t,
                method='RK45'
            )
            trajectories[i] = sol.y.T
        
        return t, trajectories
    
    def animate_chaos(self, t_span=(0, 20), dt=0.01, n_trajectories=100, 
                     trail_length=100, save_animation=False, elev=20, azim=60):
        """Create animation of diverging trajectories"""
        
        # Generate and simulate trajectories
        initial_conditions = self.generate_initial_conditions(n_trajectories)
        t, trajectories = self.simulate_trajectories(t_span, dt, initial_conditions)
        
        # Setup the figure
        self.fig = plt.figure(figsize=(12, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Set view angle
        self.ax.view_init(elev=elev, azim=azim)
        
        # Initialize lines
        self.lines = [self.ax.plot([], [], [], '-', alpha=0.5, linewidth=1)[0] 
                     for _ in range(n_trajectories)]
        
        # Color the lines according to their initial position's distance from the mean
        mean_init = np.mean(initial_conditions, axis=0)
        distances = np.linalg.norm(initial_conditions - mean_init, axis=1)
        colors = plt.cm.viridis(distances / np.max(distances))
        
        for line, color in zip(self.lines, colors):
            line.set_color(color)
        
        # Set labels and title
        self.ax.set_xlabel('X', fontsize=12)
        self.ax.set_ylabel('Y', fontsize=12)
        self.ax.set_zlabel('Z', fontsize=12)
        self.ax.set_title('Lorenz Attractor - Chaotic Behavior\n'
                         f'{n_trajectories} trajectories with nearby initial conditions',
                         fontsize=14)
        
        # Determine axis limits
        padding = 0.1
        for i in range(3):
            min_val = trajectories[:, :, i].min()
            max_val = trajectories[:, :, i].max()
            pad = padding * (max_val - min_val)
            if i == 0:
                self.ax.set_xlim([min_val - pad, max_val + pad])
            elif i == 1:
                self.ax.set_ylim([min_val - pad, max_val + pad])
            else:
                self.ax.set_zlim([min_val - pad, max_val + pad])
        
        def init():
            for line in self.lines:
                line.set_data([], [])
                line.set_3d_properties([])
            return self.lines
        
        def animate(frame):
            # Get the indices for the trail
            start_idx = max(0, frame - trail_length)
            
            # Update each trajectory
            for line, traj in zip(self.lines, trajectories):
                line.set_data(traj[start_idx:frame, 0], 
                            traj[start_idx:frame, 1])
                line.set_3d_properties(traj[start_idx:frame, 2])
            
            return self.lines
        
        # Create animation
        anim = animation.FuncAnimation(self.fig, animate, init_func=init,
                                     frames=len(t), interval=20, 
                                     blit=True)
        
        if save_animation:
            anim.save('video/lorenz_chaos.mp4', writer='ffmpeg')
        
        plt.show()
        
        return anim

# Example usage
if __name__ == "__main__":
    system = LorenzChaosAnimation()
    anim = system.animate_chaos(
        t_span=(0, 20),
        dt=0.01,
        n_trajectories=100,
        trail_length=50,
        save_animation=False,
        elev=20,
        azim=-75
    )