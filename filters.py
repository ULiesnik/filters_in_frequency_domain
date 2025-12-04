import numpy as np

# матриця відстаней від центру
def distances_matrix(_fourier):
    M, N = _fourier.shape
    m, n = M // 2, N // 2
    u = np.arange(M).reshape(-1, 1)
    v = np.arange(N).reshape(1, -1)
    return np.sqrt((u - m) ** 2 + (v - n) ** 2)

# загальна функція фільтрації
def frequency_filter(_type, _fourier, _d0, _w=None, _order=None):
    fourier = _fourier.copy()
    distances = distances_matrix(_fourier)
    return filters[_type](fourier, distances,_d0, _w, _order)


# окремі фільтри з різними H:

def ideal_lowpass_filter(_fourier, D, _d0, _w, _order):
    mask = D > _d0
    _fourier[mask] = 1
    return _fourier

def ideal_highpass_filter(_fourier, D, _d0, _w, _order):
    mask = D < _d0
    _fourier[mask] = 1
    return _fourier

def ideal_bandpass_filter(_fourier, D, _d0, _w, _order):
    mask = (D > (_d0+(_w/2))) | (D < (_d0-(_w/2)))
    _fourier[mask] = 1
    return _fourier

def ideal_bandstop_filter(_fourier, D, _d0, _w, _order):
    mask = (D < (_d0 - _w / 2)) | (D > (_d0 + _w / 2)) 
    _fourier[mask] = 1
    return _fourier


def gaussian_lowpass_filter(_fourier, D, _d0, _w, _order):
    H = np.exp(-(D ** 2) / (2 * (_d0 ** 2))) 
    return _fourier*H

def gaussian_highpass_filter(_fourier, D, _d0, _w, _order):
    H = 1 - np.exp(-(D ** 2) / (2 * (_d0 ** 2)))
    return _fourier*H

def gaussian_bandstop_filter(_fourier, D, _d0, _w, _order):
    H = 1 - np.exp(- ((D**2 - _d0**2) ** 2) / (2 * (_w ** 2) * D**2 + 1e-5))  # 1е-5 для уникнення ділення на 0
    return _fourier*H

def gaussian_bandpass_filter(_fourier, D, _d0, _w, _order):
    H = np.exp(- ((D**2 - _d0**2) ** 2) / (2 * (_w ** 2) * D**2 + 1e-5))  
    return _fourier*H


def butterworth_lowpass_filter(_fourier, D, _d0, _w, _order):
    H = 1 / (1 + ( D / _d0)**(2 * _order))
    return _fourier * H

def butterworth_highpass_filter(_fourier, D, _d0, _w, _order):
    H = 1 / (1 + (_d0 / (D + 1e-5))**(2 * _order)) 
    return _fourier * H

def butterworth_bandstop_filter(_fourier, D, _d0, _w, _order):
    H = 1 / (1 + ((_w * D) / (D**2 - _d0**2 + 1e-5))**(2 * _order)) 
    return _fourier * H

def butterworth_bandpass_filter(_fourier, D, _d0, _w, _order):
    H = 1 / (1 + ((_w * D) / (D**2 - _d0**2 + 1e-5))**(2 * _order))  
    H = 1 - H  # band-stop до band-pass
    return _fourier * H

def laplacian_filter(_fourier, D, _d0, _w, _order):
    H = -4 * (np.pi ** 2) * (D ** 2)
    return _fourier * H

def log_filter(_fourier, D, _d0, _w, _order):
    H = -4 * (np.pi ** 2) * (D ** 2) * np.exp(-2 * (np.pi ** 2) * (D ** 2) / (_d0 ** 2))
    return _fourier * H

# перелік функцій для фільтрації
filters = {
    "З ідеальним зрізом | З пропуском низьких частот":ideal_lowpass_filter,
    "З ідеальним зрізом | З пропуском високих частот":ideal_highpass_filter,
    "З ідеальним зрізом | Смуговий 1":ideal_bandpass_filter,
    "З ідеальним зрізом | Смуговий 2":ideal_bandstop_filter,
    "Гауса | З пропуском низьких частот":gaussian_lowpass_filter,
    "Гауса | З пропуском високих частот":gaussian_highpass_filter,
    "Гауса | Смуговий 1":gaussian_bandpass_filter,
    "Гауса | Смуговий 2":gaussian_bandstop_filter,
    "Баттерворта | З пропуском низьких частот":butterworth_lowpass_filter,
    "Баттерворта | З пропуском високих частот":butterworth_highpass_filter,
    "Баттерворта | Смуговий 1":butterworth_bandpass_filter,
    "Баттерворта | Смуговий 2":butterworth_bandstop_filter,
    "Лапласа | З пропуском низьких частот": laplacian_filter,
    "Лапласа від Гауса | З пропуском низьких частот": log_filter
}


