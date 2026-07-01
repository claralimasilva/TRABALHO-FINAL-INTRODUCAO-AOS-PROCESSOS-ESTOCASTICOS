"""Simulação do modelo de Ising com Metropolis-Hastings."""

import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

N = 40
K_B = 1.0
EQUIL_SWEEPS = 2000
PROD_SWEEPS = 5000
SAMPLE_INTERVAL = 10
N_CHAINS = 5
FIG_DIR = Path("figuras")
GRID_SYMBOL_STYLE = "arrows"  # "arrows" (↑/↓) ou "letters" (C/B)


def random_spins(n: int) -> np.ndarray:
    return np.random.choice([-1, 1], size=(n, n))


def compute_energy(spins: np.ndarray) -> float:
    horizontal = np.sum(spins * np.roll(spins, -1, axis=1))
    vertical = np.sum(spins * np.roll(spins, -1, axis=0))
    return float(horizontal + vertical)


def neighbor_sum(spins: np.ndarray, i: int, j: int) -> int:
    n = spins.shape[0]
    return (
        spins[i, (j + 1) % n]
        + spins[i, (j - 1) % n]
        + spins[(i + 1) % n, j]
        + spins[(i - 1) % n, j]
    )


def metropolis_sweep(spins: np.ndarray, beta: float) -> None:
    n = spins.shape[0]
    for _ in range(n * n):
        i = np.random.randint(0, n)
        j = np.random.randint(0, n)
        spin = spins[i, j]
        delta_e = -2 * spin * neighbor_sum(spins, i, j)
        if delta_e <= 0 or np.random.random() < np.exp(-beta * delta_e):
            spins[i, j] = -spin


def run_chain(
    temperature: float,
    equil_sweeps: int = EQUIL_SWEEPS,
    prod_sweeps: int = PROD_SWEEPS,
    sample_interval: int = SAMPLE_INTERVAL,
    spins: np.ndarray | None = None,
) -> tuple[np.ndarray, list[float]]:
    beta = 1.0 / (K_B * temperature)
    if spins is None:
        spins = random_spins(N)

    for _ in range(equil_sweeps):
        metropolis_sweep(spins, beta)

    energies: list[float] = []
    for step in range(prod_sweeps):
        metropolis_sweep(spins, beta)
        if (step + 1) % sample_interval == 0:
            energies.append(compute_energy(spins))

    return spins, energies


def mean_energy(
    temperature: float,
    n_chains: int = N_CHAINS,
    verbose: bool = False,
) -> float:
    chain_means: list[float] = []
    for chain in range(1, n_chains + 1):
        energies = run_chain(temperature)[1]
        chain_mean = float(np.mean(energies))
        chain_means.append(chain_mean)
        if verbose:
            print(f"    cadeia {chain}/{n_chains}: <E> = {chain_mean:.2f}", flush=True)
    return float(np.mean(chain_means))


def save_grid_figure(
    spins: np.ndarray,
    temperature: float,
    path: Path,
    style: str = GRID_SYMBOL_STYLE,
) -> None:
    n = spins.shape[0]
    fig_size = max(7.0, n * 0.18)
    fig, ax = plt.subplots(figsize=(fig_size, fig_size))

    up_color = np.array([0.30, 0.58, 0.92])
    down_color = np.array([0.91, 0.42, 0.38])
    background = np.zeros((n, n, 3))
    for i in range(n):
        for j in range(n):
            background[i, j] = up_color if spins[i, j] == 1 else down_color

    ax.imshow(background, interpolation="nearest")
    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=0.45, alpha=0.75)
    ax.tick_params(which="minor", size=0)

    if style == "letters":
        symbol_up, symbol_down = "C", "B"
        up_legend = "C --- cima ($\\sigma = +1$)"
        down_legend = "B --- baixo ($\\sigma = -1$)"
    else:
        symbol_up, symbol_down = "\u2191", "\u2193"
        up_legend = "$\\uparrow$ cima ($\\sigma = +1$)"
        down_legend = "$\\downarrow$ baixo ($\\sigma = -1$)"

    fontsize = max(5.0, min(11.0, 200.0 / n))
    for i in range(n):
        for j in range(n):
            symbol = symbol_up if spins[i, j] == 1 else symbol_down
            ax.text(
                j,
                i,
                symbol,
                ha="center",
                va="center",
                color="white",
                fontsize=fontsize,
                fontweight="bold",
            )

    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(n - 0.5, -0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Configuração em $T = {temperature}$", fontsize=14, pad=14)
    ax.legend(
        handles=[
            Patch(facecolor=up_color, edgecolor="white", label=up_legend),
            Patch(facecolor=down_color, edgecolor="white", label=down_legend),
        ],
        loc="upper right",
        fontsize=9,
        framealpha=0.92,
    )
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def save_energy_vs_temperature(
    temperatures: np.ndarray,
    mean_energies: np.ndarray,
    path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(temperatures, mean_energies, "o-", linewidth=1.5, markersize=5)
    ax.set_xlabel("Temperatura $T$")
    ax.set_ylabel("Energia média $\\langle E \\rangle$")
    ax.set_title("Energia média do sistema em função da temperatura")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    os.makedirs(FIG_DIR, exist_ok=True)
    np.random.seed(42)

    for temperature in (0.5, 2.0):
        spins, _ = run_chain(temperature)
        label = f"{temperature:.1f}".replace(".", "_")
        save_grid_figure(spins, temperature, FIG_DIR / f"grade_T{label}.png")
        print(f"Grade salva para T = {temperature}", flush=True)

    temperatures = np.linspace(0.1, 1.9, 20)
    print(
        f"Calculando energia média ({len(temperatures)} temperaturas, "
        f"{N_CHAINS} cadeias por temperatura)...",
        flush=True,
    )
    mean_energies: list[float] = []
    for i, t in enumerate(temperatures, start=1):
        print(f"[{i}/{len(temperatures)}] T = {t:.2f}", flush=True)
        e = mean_energy(t, verbose=True)
        mean_energies.append(e)
        print(f"  média final: <E> = {e:.2f}", flush=True)
    mean_energies_arr = np.array(mean_energies)
    save_energy_vs_temperature(
        temperatures,
        mean_energies_arr,
        FIG_DIR / "energia_vs_T.png",
    )
    print("Gráfico energia vs temperatura salvo.", flush=True)

    print("\nResumo:", flush=True)
    for t, e in zip(temperatures, mean_energies_arr):
        print(f"T = {t:.2f}, <E> = {e:.2f}", flush=True)


if __name__ == "__main__":
    main()
