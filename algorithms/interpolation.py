from math import pow, sin, cos, pi, sqrt

'''
Here is a good source for different interpolation functions in Java:
https://github.com/libgdx/libgdx/blob/master/gdx/src/com/badlogic/gdx/math/Interpolation.java
'''

def getInterpolationPreset(name = "LINEAR", easeIn = True, easeOut = True):
    if not (easeIn or easeOut): return (linear, None)
    if name == "LINEAR": return (linear, None)
    if name == "SINUSOIDAL":
        if easeIn and easeOut: return (sinInOut, None)
        if easeIn: return (sinIn, None)
        return (sinOut, None)
    if name in exponentOfName.keys():
        if easeIn and easeOut: return (powerInOut, exponentOfName[name])
        if easeIn: return (powerIn, exponentOfName[name])
        return (powerOut, exponentOfName[name])
    if name == "EXPONENTIAL":
        if easeIn and easeOut: return (exponentialInOut, (2.0, 5.0))
        if easeIn: return (exponentialIn, (2.0, 5.0))
        return (exponentialOut, (2.0, 5.0))
    if name == "CIRCULAR":
        if easeIn and easeOut: return (circularInOut, None)
        if easeIn: return (circularIn, None)
        return (circularOut, None)
    if name == "BACK":
        if easeIn and easeOut: return (backInOut, 1.7)
        if easeIn: return (backIn, 1.7)
        return (backOut, 1.7)
    if name == "BOUNCE":
        if easeIn and easeOut: return (bounceInOut, None)
        if easeIn: return (bounceIn, None)
        return (bounceOut, None)
    if name == "ELASTIC":
        if easeIn and easeOut: return (elasticInOut, (1.44, 5.06, 4.46, -1.0))
        if easeIn: return (elasticIn, (1.44, 5.06, 4.46, -1.0))
        return (elasticOut, (1.44, 5.06, 4.46, -1.0))

exponentOfName = {
    "QUADRATIC" : 2,
    "CUBIC" : 3,
    "QUARTIC" : 4,
    "QUINTIC" : 5 }


# Linear interpolation

def linear(x, settings = None):
    return x


# Power interpolation

def powerInOut(x, exponent = 2):
    '''Exponent has to be a positive integer'''
    if x <= 0.5:
        return pow(x * 2, exponent) / 2
    else:
        return pow((x - 1) * 2, exponent) / (-2 if exponent % 2 == 0 else 2) + 1

def powerIn(x, exponent = 2):
    return pow(x, exponent)

def powerOut(x, exponent = 2):
    return pow(x - 1, exponent) * (-1 if exponent % 2 == 0 else 1) + 1


# Exponential interpolation

def exponentialInOut(x, settings):
    value, exponent = settings
    minValue = pow(value, -exponent)
    scale = 1 / (1 - minValue)

    if x <= 0.5:
        return (pow(value, exponent * (x * 2 - 1)) - minValue) * scale / 2
    else:
        return (2 - (pow(value, -exponent * (x * 2 - 1)) - minValue) * scale) / 2

def exponentialIn(x, settings):
    value, exponent = settings
    minValue = pow(value, -exponent)
    scale = 1 / (1 - minValue)

    return (pow(value, exponent * (x - 1)) - minValue) * scale

def exponentialOut(x, settings):
    value, exponent = settings
    minValue = pow(value, -exponent)
    scale = 1 / (1 - minValue)

    return 1 - (pow(value, -exponent * x) - minValue) * scale


# Circle interpolation

def circularInOut(x, settings = None):
    if x <= 0.5:
        x *= 2
        return (1 - sqrt(1 - x * x)) / 2
    else:
        x = (x - 1) * 2
        return (sqrt(1 - x * x) + 1) / 2

def circularIn(x, settings = None):
    return 1 - sqrt(1 - x * x)

def circularOut(x, settings = None):
    x -= 1
    return sqrt(1 - x * x)


# Elastic interpolation

def elasticInOut(x, settings):
    '''
    value > 0
    '''
    value, exponent, bounces, scale = settings
    bounces = bounces * pi * (1 if bounces % 2 == 0 else -1)
    if x <= 0.5:
        x *= 2
        return pow(value, exponent * (x - 1)) * sin(x * bounces) * scale / 2
    else:
        x = (1 - x) * 2
        return 1 - pow(value, exponent * (x - 1)) * sin(x * bounces) * scale / 2

def elasticIn(x, settings):
    '''
    scale should be -1 or 1 depending on bounces
    '''
    value, exponent, bounces, scale = settings
    bounces = bounces * pi * (1 if bounces % 2 == 0 else -1)

    return pow(value, exponent * (x - 1)) * sin(x * bounces) * scale

def elasticOut(x, settings):
    value, exponent, bounces, scale = settings
    bounces = bounces * pi * (1 if bounces % 2 == 0 else -1)

    x = 1 - x
    return 1 - pow(value, exponent * (x - 1)) * sin(x * bounces) * scale


# Bounce interpolation

widths = [0.68, 0.34, 0.2, 0.12] # should follow this rule: 1 = sum(widths) - widths[0] / 2
heights = [1.0, 0.26, 0.11, 0.03]

def bounceInOut(x, settings = None):
    if x <= 0.5: return (1 - bounceOut(1 - x * 2)) / 2
    else: return bounceOut(x * 2 - 1) / 2 + 0.5

def bounceIn(x, settings = None):
    return 1 - bounceOut(1 - x)

def bounceOut(x, settings = None):
    x += widths[0] / 2
    for width, height in zip(widths, heights):
        if x <= width: break
        x -= width
    x /= width
    z = 4 / width * height * x
    return 1 -(z - z * x) * width



# Back swing interpolation

def backInOut(x, scale = 1.7):
    if x <= 0.5:
        x *= 2
        return x * x * ((scale + 1) * x - scale) / 2
    else:
        x = (x - 1) * 2
        return x * x * ((scale + 1) * x + scale) / 2 + 1

def backIn(x, scale = 1.7):
    return x * x * ((scale + 1) * x - scale)

def backOut(x, scale = 1.7):
    x -= 1
    return x * x * ((scale + 1) * x + scale) + 1


# Sine interpolation

def sinInOut(x, settings = None):
    return (1 - cos(x * pi)) / 2

def sinIn(x, settings = None):
    return 1 - cos(x * pi / 2)

def sinOut(x, settings = None):
    return sin(x * pi / 2)


# Specials

def curveInterpolation(x, settings):
    try:
        return (settings[0].evaluate(x) - 0.25)*2
    except:
        settings[1].initialize()
        return (settings[0].evaluate(x) - 0.25)*2

def mixedInterpolation(x, settings):
    a, b, factor = settings
    return a[0](x, a[1]) * (1 - factor) + b[0](x, b[1]) * factor
