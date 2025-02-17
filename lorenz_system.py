import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

class LorenzObserverSystem:
    def __init__(self, sigma=10, rho=28, beta=8/3, noise_std=1.0):
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        self.noise_std = noise_std
    
    def lorenz_plant(self, t, state):
        """Original Lorenz system"""
        x, y, z = state
        dx = self.sigma * (y - x)
        dy = self.rho * x - y - x * z 
        dz = x * y - self.beta * z
        return [dx, dy, dz]
    
    def observer_yz(self, t, state, x_meas):
        """YZ observer system"""
        y_hat, z_hat = state
        dy_hat = self.rho * x_meas - y_hat - x_meas * z_hat
        dz_hat = -self.beta * z_hat + x_meas * y_hat
        return [dy_hat, dz_hat]
    
    def observer_x(self, t, state, y_hat):
        """X observer system"""
        x_hat = state[0]
        dx_hat = self.sigma * (y_hat - x_hat)
        return [dx_hat]
    
    def add_noise(self, x):
        """Add Gaussian noise to measurement"""
        return x + np.random.normal(0, self.noise_std)
    
    def simulate(self, t_span, dt):
        """Simulate the complete system"""
        t = np.arange(t_span[0], t_span[1], dt)
        
        # Arrays to store results
        plant_states = np.zeros((len(t), 3))
        observer_states = np.zeros((len(t), 3))
        noisy_measurements = np.zeros(len(t))
        
        # Initial conditions
        plant_states[0] = [1.0, 1.0, 1.0]  # x, y, z
        observer_states[0] = [0.0, 0.0, 0.0]  # x_hat, y_hat, z_hat
        noisy_measurements[0] = self.add_noise(plant_states[0, 0])
        
        # Step through time to match block diagram structure
        for i in range(1, len(t)):
            # 1. Integrate plant for one step
            plant_sol = solve_ivp(
                self.lorenz_plant,
                [t[i-1], t[i]],
                plant_states[i-1],
                method='RK45'
            )
            plant_states[i] = plant_sol.y[:, -1]
            
            # 2. Add noise to x measurement
            noisy_measurements[i] = self.add_noise(plant_states[i, 0])
            
            # 3. Integrate YZ observer using noisy x measurement
            yz_sol = solve_ivp(
                lambda t, state: self.observer_yz(t, state, noisy_measurements[i]),
                [t[i-1], t[i]],
                observer_states[i-1, 1:],
                method='RK45'
            )
            
            # 4. Integrate X observer using estimated y
            x_sol = solve_ivp(
                lambda t, state: self.observer_x(t, state, yz_sol.y[0, -1]),
                [t[i-1], t[i]],
                [observer_states[i-1, 0]],
                method='RK45'
            )
            
            # Store results
            observer_states[i] = [x_sol.y[0, -1], yz_sol.y[0, -1], yz_sol.y[1, -1]]
            
        return t, plant_states, observer_states, noisy_measurements
    
    def calculate_errors(self, plant_states, observer_states):
        """Calculate estimation errors"""
        return observer_states - plant_states
    
    def plot_results(self, t, plant_states, observer_states, noisy_measurements):
        """Plot the state estimates and combined errors"""
        errors = self.calculate_errors(plant_states, observer_states)
        
        # Create 4 subplots:
        #  - 3 for the state variables (x, y, z)
        #  - 1 for all three error curves together
        fig, axs = plt.subplots(4, 1, figsize=(9, 7))
        
        # Plot x state and measurement
        axs[0].plot(t, plant_states[:, 0], 'b-', label='True x')
        axs[0].plot(t, observer_states[:, 0], 'r--', label='Estimated x')
        axs[0].plot(t, noisy_measurements, 'g:', label='Noisy x measurement')
        axs[0].set_ylabel('x')
        axs[0].legend()
        axs[0].grid(True)
        
        # Plot y state
        axs[1].plot(t, plant_states[:, 1], 'b-', label='True y')
        axs[1].plot(t, observer_states[:, 1], 'r--', label='Estimated y')
        axs[1].set_ylabel('y')
        axs[1].legend()
        axs[1].grid(True)
        
        # Plot z state
        axs[2].plot(t, plant_states[:, 2], 'b-', label='True z')
        axs[2].plot(t, observer_states[:, 2], 'r--', label='Estimated z')
        axs[2].set_ylabel('z')
        axs[2].legend()
        axs[2].grid(True)
        
        # Plot combined errors for x, y, and z
        axs[3].plot(t, errors[:, 0], 'k-', label='x error')
        axs[3].plot(t, errors[:, 1], 'm-', label='y error')
        axs[3].plot(t, errors[:, 2], 'c-', label='z error')
        axs[3].set_ylabel('Error')
        axs[3].set_xlabel('Time')
        axs[3].legend()
        axs[3].grid(True)
        
        plt.tight_layout()
        return fig, axs

# Example usage
if __name__ == "__main__":
    system = LorenzObserverSystem()
    t, plant_states, observer_states, noisy_measurements = system.simulate((0, 10), 0.01)
    fig, axs = system.plot_results(t, plant_states, observer_states, noisy_measurements)
    plt.show()