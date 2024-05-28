import numpy as np
import matplotlib.pyplot as plt


def fraunhofer_diffraction(
        amplitude_distribution,
        name,
        L=1.0,  # Расстояние до экрана (м)
        λ=0.5e-6,  # Длина волны (м)
):
    N = amplitude_distribution.shape[0]
    D = 1.0  # Предполагаемый диаметр апертуры для нормализации координат
    dx = D / N  # Размер шага (м)

    # Преобразование Фурье
    fft_result = np.fft.fftshift(np.fft.fft2(amplitude_distribution))
    # fft_result = fft_result / np.max(np.abs(fft_result))  # Нормализация
    print(f"Максимальное значение после FFT: {np.max(np.abs(fft_result))}")

    # Координаты в дальней плоскости
    x_fraunhofer = np.fft.fftshift(np.fft.fftfreq(N, dx)) * λ * L
    y_fraunhofer = np.fft.fftshift(np.fft.fftfreq(N, dx)) * λ * L
    x_fraunhofer, y_fraunhofer = np.meshgrid(x_fraunhofer, y_fraunhofer)

    # Расчет интенсивности
    intensity = np.abs(fft_result) ** 2

    # Визуализация амплитудного распределения
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(amplitude_distribution, extent=(-D / 2, D / 2, -D / 2, D / 2), cmap='gray')
    plt.title('Amplitude Distribution')
    plt.colorbar()

    # Визуализация распределения интенсивности
    plt.subplot(1, 2, 2)
    plt.imshow(np.log1p(intensity), extent=(x_fraunhofer.min(), x_fraunhofer.max(),
                                            y_fraunhofer.min(), y_fraunhofer.max()),
               cmap='inferno')
    plt.title('Intensity Distribution (Fraunhofer Diffraction)')
    plt.colorbar()

    plt.savefig(name)


if __name__ == '__main__':
    # L = float(input('Введите L в мм: \n')) * 1.0e-3
    # λ = float(input('Введите λ в нм: \n')) * 1.0e-9
    # N = int(input('Введите размера массива двумерного амплитудного распределения N: \n'))
    # D = float(input('Введите диаметр апертуры'))

    L = 0.5
    λ = 500 * 1.0e-9
    N = 1000  # Размер массива
    D = 0.5  # Диаметр апертуры (м)
    dx = D / N  # Размер шага (м)
    x = np.linspace(-D / 2, D / 2, N)
    y = np.linspace(-D / 2, D / 2, N)
    x, y = np.meshgrid(x, y)

    # r1 = np.sqrt((x + 0.1) ** 2 + (y + 0.1) ** 2)  # Смещенный круг
    # r2 = np.sqrt((x - 0.2) ** 2 + (y - 0.2) ** 2)  # Другой смещенный круг
    # r3 = np.sqrt((x + 0.3) ** 2 + (y - 0.3) ** 2)  # Третий круг
    # r4 = np.sqrt((x - 0.4) ** 2 + (y + 0.4) ** 2)  # Четвертый круг
    # amplitude_distribution = np.where((r1 <= 0.15) | (r2 <= 0.1) | (r3 <= 0.05) | (r4 <= 0.2), 0, 1)

    # одна щель
    slit_width = 0.05
    amplitude_distribution = np.where(np.abs(x) <= slit_width / 2, 1, 0)
    fraunhofer_diffraction(amplitude_distribution, "single_slit", L, λ)
    # # Создание амплитудного распределения для нескольких щелей
    # slit_width = 0.05  # Ширина каждой щели (м)
    # slit_spacing = 1  # Расстояние между центрами щелей (м)
    # num_slits = 2  # Количество щелей
    #
    # amplitude_distribution = np.zeros_like(x)
    # for i in range(num_slits):
    #     center = -slit_spacing * (num_slits // 2) + i * slit_spacing
    #     amplitude_distribution += np.where(np.abs(x - center) <= slit_width / 2, 1, 0)

    r = np.sqrt(x ** 2 + y ** 2)
    amplitude_distribution = np.where(r <= D / 2, 1, 0)
    fraunhofer_diffraction(amplitude_distribution, "circle_hole", L, λ)
