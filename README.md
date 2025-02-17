# Contraction-based Observer Design for the Lorenz System
This repository demonstrates the robustness properties of contracting systems through the implementation of a reduced-order contracting observer for the 3D Lorenz system using only 1D noisy measurements. It includes visualizations of both the chaotic nature of the Lorenz system and the performance of the observer under noisy conditions.

[Watch videos here](https://sajad2025.github.io/lorenz_observer/)

# Background
## Contraction Theory
[Lohmiller, W. and Slotine, J.J.E., 1998. On contraction analysis for non-linear systems. Automatica, 34(6), pp.683-696.](https://web.mit.edu/nsl/www/preprints/contraction.pdf)

[Slotine, J.J.E., 2003. Modular stability tools for distributed computation and control. International Journal of Adaptive Control and Signal Processing, 17(6), pp.397-416.](https://web.mit.edu/nsl/www/preprints/modular.pdf)

[Wang, W. and Slotine, J.J.E., 2005. On partial contraction analysis for coupled nonlinear oscillators. Biological cybernetics, 92(1), pp.38-53.](https://web.mit.edu/nsl/www/preprints/BioCyb04.pdf)

[Tsukamoto, H., Chung, S.J. and Slotine, J.J.E., 2021. Contraction theory for nonlinear stability analysis and learning-based control: A tutorial overview. Annual Reviews in Control, 52, pp.135-169.](https://arxiv.org/pdf/2110.00675)

## Lorenz System
The Lorenz system is a system of ordinary differential equations known for exhibiting chaotic behavior. The system is described by:

$$
\begin{aligned}
\dot{x} &= \sigma(y - x) \\
\dot{y} &= \rho x -y  -xz \\
\dot{z} &= -\beta z +xy
\end{aligned}
$$

where σ, ρ, and β are system parameters. Classic values are σ = 10, ρ = 28, and β = 8/3.

## Observer YZ
Consider the following reduced-order observer ([Slotine, 2003](https://web.mit.edu/nsl/www/preprints/modular.pdf)), with noisy measurement of $[x]$ as input and estimated signals of $[\hat{y}, \hat{z}]$ as output: 

$$\begin{aligned}
\dot{\hat{y}} &= \rho \,x_m -\hat{y}  -x_m \,\hat{z} \\
\dot{\hat{z}} &= -\beta \,\hat{z} +x_m \,\hat{y}
\end{aligned}$$

where $x_m = x + \eta$, and $\eta \sim \mathcal{N}(0, 1.0)$ is the measurement noise.

The symmetric part of the Jacobian for this reduced-order observer is $diag(-1, -\beta)$ which is negative definite, meaning the observer is contracting.

The above auxiliary virtual observer system ([Wang and Slotine, 2005](https://web.mit.edu/nsl/www/preprints/BioCyb04.pdf)), has $[x,y,z]$ and $[x,\hat{y}, \hat{z}]$ as its particular solutions.

Contracting systems converge exponentially, exhibiting superior robustness properties ([Tsukamoto, Chung and Slotine, 2021](https://arxiv.org/pdf/2110.00675)), providing explicit bounds on the distance between the real system trajectory $[x,y,z]$ and the perturbed system $[x_m, \hat{y}, \hat{z}]$.  

## Hierarchical Combination, Observer X
Now we can construct the following augmented dynamics to clean the noise on the measured $[x]$ state, resulting in a hierarchy of two contracting systems ([Slotine, 2003](https://web.mit.edu/nsl/www/preprints/modular.pdf)), where the estimated $[\hat{y}]$ signal is fed into the following augmented observer system in series:

$$\begin{aligned} \dot{\hat{x}} &= \sigma (\hat{y}  -\hat{x}) \\ \end{aligned}$$

# Repository Structure
```
lorenz_observer/
├── README.md
├── requirements.txt
├── lorenz_system.py                # Base Lorenz system implementation
├── lorenz_animation_chaos.py       # Animation, chaotic nature of the Lorenz system
└── lorenz_animation_observer.py    # Animation, observer performance
└── docs/
    ├── index.html                  # HTML file with embedded videos
    └── videos/
        ├── lorenz_chaos.mp4        # Video 1: Lorenz chaos demo
        └── lorenz_observer.mp4     # Video 2: Observer performance demo
```

# Installation

1. Clone the repository:
```bash
git clone https://github.com/sajad2025/lorenz_observer.git
cd lorenz_observer
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

# Usage

### Running the Observer Animation
```python
python3 lorenz_animation_observer.py
```

This will show the animation of the Lorenz system with the observer, including two measurement planes:
- Blue plane: True x-coordinate
- Red plane: Noisy measurement of x-coordinate

### Running the Chaos Demonstration
```python
python3 lorenz_animation_chaos.py
```

This will show multiple trajectories starting from nearby initial conditions, demonstrating the chaotic nature of the Lorenz system.

## Dependencies
- numpy
- scipy
- matplotlib

These can be installed via the requirements.txt file.

## Optional Dependencies
For saving animations, recommended for MP4 output:
- ffmpeg 

```bash
# On macOS using Homebrew
brew install ffmpeg

# On Ubuntu/Debian
sudo apt-get install ffmpeg

# On Windows using Chocolatey
choco install ffmpeg
```

## Parameters
Key parameters that can be adjusted:
- System parameters (σ, ρ, β)
- Noise standard deviation
- Animation view angles
- Trail length in visualizations

These can be modified in the respective Python files or passed as arguments to the animation functions.

## Contributing
Feel free to open issues or submit pull requests with improvements.

## License
This project is licensed under the MIT License - see the LICENSE file for details.