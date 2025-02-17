import numpy as np
from lorenz_system import LorenzObserverSystem
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

class LorenzObserverAnimation(LorenzObserverSystem):
    def update_planes(self, true_x, noisy_x):
        """Helper function to update the measurement planes with enhanced visibility"""
        if self.true_plane is not None:
            self.true_plane.remove()
        if self.meas_plane is not None:
            self.meas_plane.remove()
        
        # True state plane (light blue)
        self.true_plane = self.ax.plot_surface(
            np.ones_like(self.Y) * true_x, self.Y, self.Z,
            alpha=0.3,  # Increased opacity
            color='royalblue',  # More distinctive blue
            edgecolor='blue',  # Blue edges
            linewidth=0.5,  # Edge line width
            shade=True  # Enable shading for better 3D appearance
        )
        
        # Noisy measurement plane (light red)
        self.meas_plane = self.ax.plot_surface(
            np.ones_like(self.Y) * noisy_x, self.Y, self.Z,
            alpha=0.3,  # Increased opacity
            color='lightcoral',  # Changed to light red for better contrast
            edgecolor='red',  # Red edges
            linewidth=0.5,  # Edge line width
            shade=True  # Enable shading for better 3D appearance
        )

    def animate_3d(self, t, plant_states, observer_states, noisy_measurements, 
                   trail_length=500, save_animation=False, elev=30, azim=45):
        """
        Create 3D animation with enhanced measurement planes and fixed view angle
        """
        self.fig = plt.figure(figsize=(12, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Set fixed view angle
        self.ax.view_init(elev=elev, azim=azim)
        
        # Initialize lines with increased visibility
        self.true_line, = self.ax.plot([], [], [], 'b-', 
                                      label='true state', 
                                      alpha=1.0,  # Full opacity for lines
                                      linewidth=2)
        self.obs_line, = self.ax.plot([], [], [], 'r--', 
                                     label='observer state', 
                                     alpha=1.0,  # Full opacity for lines
                                     linewidth=2)
        
        # Create measurement planes
        y_range = np.array([plant_states[:, 1].min(), plant_states[:, 1].max()])
        z_range = np.array([plant_states[:, 2].min(), plant_states[:, 2].max()])
        self.Y, self.Z = np.meshgrid(y_range, z_range)
        
        # Initialize empty planes
        self.true_plane = None
        self.meas_plane = None
        
        # Set labels and title with increased font size
        self.ax.set_xlabel('X', fontsize=12)
        self.ax.set_ylabel('Y', fontsize=12)
        self.ax.set_zlabel('Z', fontsize=12)
        self.ax.set_title("Lorenz System Observer Design - Contraction Theory" +  
                            "\n added meas noise: N(μ=0, σ=1.0)", fontsize=14)
        
        # Determine axis limits with padding
        padding = 0.1
        x_min = min(plant_states[:, 0].min(), noisy_measurements.min())
        x_max = max(plant_states[:, 0].max(), noisy_measurements.max())
        y_min, y_max = plant_states[:, 1].min(), plant_states[:, 1].max()
        z_min, z_max = plant_states[:, 2].min(), plant_states[:, 2].max()
        
        self.ax.set_xlim([x_min - padding * abs(x_min), x_max + padding * abs(x_max)])
        self.ax.set_ylim([y_min - padding * abs(y_min), y_max + padding * abs(y_max)])
        self.ax.set_zlim([z_min - padding * abs(z_min), z_max + padding * abs(z_max)])
        
        # Add custom legend with updated colors
        from matplotlib.patches import Patch
        legend_elements = [
            plt.Line2D([0], [0], color='blue', label='true state'),
            plt.Line2D([0], [0], color='red', linestyle='--', label='observer state'),
            Patch(facecolor='royalblue', alpha=0.3, label='true x'),
            Patch(facecolor='lightcoral', alpha=0.3, label='noisy meas x')
        ]
        self.ax.legend(handles=legend_elements, fontsize=10)
        
        # Set grid for better depth perception
        self.ax.grid(True)
        
        def init():
            self.true_line.set_data([], [])
            self.true_line.set_3d_properties([])
            
            self.obs_line.set_data([], [])
            self.obs_line.set_3d_properties([])
            
            self.update_planes(plant_states[0, 0], noisy_measurements[0])
            
            return self.true_line, self.obs_line
        
        def animate(frame):
            start_idx = max(0, frame - trail_length)
            
            # Update trajectories
            self.true_line.set_data(plant_states[start_idx:frame, 0], 
                                  plant_states[start_idx:frame, 1])
            self.true_line.set_3d_properties(plant_states[start_idx:frame, 2])
            
            self.obs_line.set_data(observer_states[start_idx:frame, 0], 
                                 observer_states[start_idx:frame, 1])
            self.obs_line.set_3d_properties(observer_states[start_idx:frame, 2])
            
            # Update measurement planes
            self.update_planes(plant_states[frame, 0], noisy_measurements[frame])
            
            return self.true_line, self.obs_line
        
        # Create animation
        anim = animation.FuncAnimation(self.fig, animate, init_func=init,
                                     frames=len(t), interval=20, 
                                     blit=False)
        
        if save_animation:
            #anim.save('lorenz_observer.mp4', writer='ffmpeg')
            anim.save('video/lorenz_observer.html', writer='html')
        
        plt.show()
        
        return anim

# Example usage
if __name__ == "__main__":
    system = LorenzObserverAnimation()
    t, plant_states, observer_states, noisy_measurements = system.simulate(
        t_span=(0, 30),
        dt=0.01
    )
    
    anim = system.animate_3d(
        t, 
        plant_states, 
        observer_states, 
        noisy_measurements,
        trail_length=500,
        save_animation=True,
        elev=20,
        azim=-75
    )