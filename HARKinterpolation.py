'''
Custom interpolation methods for representing approximations to functions.
It also includes wrapper classes to enforce standard methods across classes.
Each interpolation class must have a distance() method that compares itself to
another instance; this is used in HARKcore's solve() method to check for solution
convergence.  The interpolator classes currently in this module inherit their
distance method from HARKobject.
'''

import numpy as np
from HARKcore import HARKobject
from HARKutilities import CRRAutility, CRRAutilityP, CRRAutility_invP
from copy import deepcopy

def _isscalar(x):
    '''
    Check whether x is if a scalar type, or 0-dim.
    
    Parameters
    ----------
    x : anything
        An input to be checked for scalar-ness.
        
    Returns
    -------
    is_scalar : boolean
        True if the input is a scalar, False otherwise.
    '''
    return np.isscalar(x) or hasattr(x, 'shape') and x.shape == ()


class HARKinterpolator1D(HARKobject):
    '''
    A wrapper class for 1D interpolation methods in HARK.
    '''
    distance_criteria = []
    
    def __call__(self,x):
        '''
        Evaluates the interpolated function at the given input.
        
        Parameters
        ----------
        x : np.array or float
            Real values to be evaluated in the interpolated function.
        
        Returns
        -------
        y : np.array or float
            The interpolated function evaluated at x: y = f(x), with the same
            shape as x.
        '''
        z = np.asarray(x)
        return (self._evaluate(z.flatten())).reshape(z.shape)
        
    def derivative(self,x):
        '''
        Evaluates the derivative of the interpolated function at the given input.
        
        Parameters
        ----------
        x : np.array or float
            Real values to be evaluated in the interpolated function.
        
        Returns
        -------
        dydx : np.array or float
            The interpolated function's first derivative evaluated at x:
            dydx = f'(x), with the same shape as x.
        '''
        z = np.asarray(x)
        return (self._der(z.flatten())).reshape(z.shape)
        
    def eval_with_derivative(self,x):
        '''
        Evaluates the interpolated function and its derivative at the given input.
        
        Parameters
        ----------
        x : np.array or float
            Real values to be evaluated in the interpolated function.
        
        Returns
        -------
        y : np.array or float
            The interpolated function evaluated at x: y = f(x), with the same
            shape as x.
        dydx : np.array or float
            The interpolated function's first derivative evaluated at x:
            dydx = f'(x), with the same shape as x.
        '''
        z = np.asarray(x)
        y, dydx = self._evalAndDer(z.flatten())
        return y.reshape(z.shape), dydx.reshape(z.shape)
        
    def _evaluate(self,x):
        '''
        Interpolated function evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()
        
    def _der(self,x):
        '''
        Interpolated function derivative evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()
        
    def _evalAndDer(self,x):
        '''
        Interpolated function and derivative evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()

       
class HARKinterpolator2D(HARKobject):
    '''
    A wrapper class for 2D interpolation methods in HARK.
    '''
    distance_criteria = []
    
    def __call__(self,x,y):
        '''
        Evaluates the interpolated function at the given input.
        
        Parameters
        ----------
        x : np.array or float
            Real values to be evaluated in the interpolated function.
        y : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as x.
        
        Returns
        -------
        fxy : np.array or float
            The interpolated function evaluated at x,y: fxy = f(x,y), with the
            same shape as x and y.
        '''
        xa = np.asarray(x)
        ya = np.asarray(y)
        return (self._evaluate(xa.flatten(),ya.flatten())).reshape(xa.shape)
        
    def derivativeX(self,x,y):
        '''
        Evaluates the partial derivative of interpolated function with respect
        to x (the first argument) at the given input.
        
        Parameters
        ----------
        x : np.array or float
            Real values to be evaluated in the interpolated function.
        y : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as x.
        
        Returns
        -------
        dfdx : np.array or float
            The derivative of the interpolated function with respect to x, eval-
            uated at x,y: dfdx = f_x(x,y), with the same shape as x and y.
        '''
        xa = np.asarray(x)
        ya = np.asarray(y)
        return (self._derX(xa.flatten(),ya.flatten())).reshape(xa.shape)
        
    def derivativeY(self,x,y):
        '''
        Evaluates the partial derivative of interpolated function with respect
        to y (the second argument) at the given input.
        
        Parameters
        ----------
        x : np.array or float
            Real values to be evaluated in the interpolated function.
        y : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as x.
        
        Returns
        -------
        dfdy : np.array or float
            The derivative of the interpolated function with respect to y, eval-
            uated at x,y: dfdx = f_y(x,y), with the same shape as x and y.
        '''
        xa = np.asarray(x)
        ya = np.asarray(y)
        return (self._derY(xa.flatten(),ya.flatten())).reshape(xa.shape)
        
    def _evaluate(self,x,y):
        '''
        Interpolated function evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()
        
    def _derX(self,x,y):
        '''
        Interpolated function x-derivative evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()
        
    def _derY(self,x,y):
        '''
        Interpolated function y-derivative evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()

        
class HARKinterpolator3D(HARKobject):
    '''
    A wrapper class for 3D interpolation methods in HARK.
    '''
    distance_criteria = []
    
    def __call__(self,x,y,z):
        '''
        Evaluates the interpolated function at the given input.
        
        Parameters
        ----------
        x : np.array or float
            Real values to be evaluated in the interpolated function.
        y : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as x.
        z : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as x.
        
        Returns
        -------
        fxyz : np.array or float
            The interpolated function evaluated at x,y,z: fxyz = f(x,y,z), with
            the same shape as x, y, and z.
        '''
        xa = np.asarray(x)
        ya = np.asarray(y)
        za = np.asarray(z)
        return (self._evaluate(xa.flatten(),ya.flatten(),za.flatten())).reshape(xa.shape)
        
    def derivativeX(self,x,y,z):
        '''
        Evaluates the partial derivative of the interpolated function with respect
        to x (the first argument) at the given input.
        
        Parameters
        ----------
        x : np.array or float
            Real values to be evaluated in the interpolated function.
        y : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as x.
        z : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as x.
        
        Returns
        -------
        dfdx : np.array or float
            The derivative with respect to x of the interpolated function evaluated
            at x,y,z: dfdx = f_x(x,y,z), with the same shape as x, y, and z.
        '''
        xa = np.asarray(x)
        ya = np.asarray(y)
        za = np.asarray(z)
        return (self._derX(xa.flatten(),ya.flatten(),za.flatten())).reshape(xa.shape)
        
    def derivativeY(self,x,y,z):
        '''
        Evaluates the partial derivative of the interpolated function with respect
        to y (the second argument) at the given input.
        
        Parameters
        ----------
        x : np.array or float
            Real values to be evaluated in the interpolated function.
        y : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as x.
        z : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as x.
        
        Returns
        -------
        dfdy : np.array or float
            The derivative with respect to y of the interpolated function evaluated
            at x,y,z: dfdy = f_y(x,y,z), with the same shape as x, y, and z.
        '''
        xa = np.asarray(x)
        ya = np.asarray(y)
        za = np.asarray(z)
        return (self._derY(xa.flatten(),ya.flatten(),za.flatten())).reshape(xa.shape)
        
    def derivativeZ(self,x,y,z):
        '''
        Evaluates the partial derivative of the interpolated function with respect
        to z (the third argument) at the given input.
        
        Parameters
        ----------
        x : np.array or float
            Real values to be evaluated in the interpolated function.
        y : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as x.
        z : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as x.
        
        Returns
        -------
        dfdz : np.array or float
            The derivative with respect to z of the interpolated function evaluated
            at x,y,z: dfdz = f_z(x,y,z), with the same shape as x, y, and z.
        '''
        xa = np.asarray(x)
        ya = np.asarray(y)
        za = np.asarray(z)
        return (self._derZ(xa.flatten(),ya.flatten(),za.flatten())).reshape(xa.shape)
        
    def _evaluate(self,x,y,z):
        '''
        Interpolated function evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()
        
    def _derX(self,x,y,z):
        '''
        Interpolated function x-derivative evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()
        
    def _derY(self,x,y,z):
        '''
        Interpolated function y-derivative evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()
        
    def _derZ(self,x,y,z):
        '''
        Interpolated function y-derivative evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()
        
        
class HARKinterpolator4D(HARKobject):
    '''
    A wrapper class for 4D interpolation methods in HARK.
    '''
    distance_criteria = []
    
    def __call__(self,w,x,y,z):
        '''
        Evaluates the interpolated function at the given input.
        
        Parameters
        ----------
        w : np.array or float
            Real values to be evaluated in the interpolated function.
        x : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        y : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        z : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        
        Returns
        -------
        fwxyz : np.array or float
            The interpolated function evaluated at w,x,y,z: fwxyz = f(w,x,y,z),
            with the same shape as w, x, y, and z.
        '''
        wa = np.asarray(w)
        xa = np.asarray(x)
        ya = np.asarray(y)
        za = np.asarray(z)
        return (self._evaluate(wa.flatten(),xa.flatten(),ya.flatten(),za.flatten())).reshape(wa.shape)

    def derivativeW(self,w,x,y,z):
        '''
        Evaluates the partial derivative with respect to w (the first argument)
        of the interpolated function at the given input.
        
        Parameters
        ----------
        w : np.array or float
            Real values to be evaluated in the interpolated function.
        x : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        y : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        z : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        
        Returns
        -------
        dfdw : np.array or float
            The derivative with respect to w of the interpolated function eval-
            uated at w,x,y,z: dfdw = f_w(w,x,y,z), with the same shape as inputs.
        '''
        wa = np.asarray(w)
        xa = np.asarray(x)
        ya = np.asarray(y)
        za = np.asarray(z)
        return (self._derW(wa.flatten(),xa.flatten(),ya.flatten(),za.flatten())).reshape(wa.shape)

    def derivativeX(self,w,x,y,z):
        '''
        Evaluates the partial derivative with respect to x (the second argument)
        of the interpolated function at the given input.
        
        Parameters
        ----------
        w : np.array or float
            Real values to be evaluated in the interpolated function.
        x : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        y : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        z : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        
        Returns
        -------
        dfdx : np.array or float
            The derivative with respect to x of the interpolated function eval-
            uated at w,x,y,z: dfdx = f_x(w,x,y,z), with the same shape as inputs.
        '''
        wa = np.asarray(w)
        xa = np.asarray(x)
        ya = np.asarray(y)
        za = np.asarray(z)
        return (self._derX(wa.flatten(),xa.flatten(),ya.flatten(),za.flatten())).reshape(wa.shape)
        
    def derivativeY(self,w,x,y,z):
        '''
        Evaluates the partial derivative with respect to y (the third argument)
        of the interpolated function at the given input.
        
        Parameters
        ----------
        w : np.array or float
            Real values to be evaluated in the interpolated function.
        x : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        y : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        z : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        
        Returns
        -------
        dfdy : np.array or float
            The derivative with respect to y of the interpolated function eval-
            uated at w,x,y,z: dfdy = f_y(w,x,y,z), with the same shape as inputs.
        '''
        wa = np.asarray(w)
        xa = np.asarray(x)
        ya = np.asarray(y)
        za = np.asarray(z)
        return (self._derY(wa.flatten(),xa.flatten(),ya.flatten(),za.flatten())).reshape(wa.shape)

    def derivativeZ(self,w,x,y,z):
        '''
        Evaluates the partial derivative with respect to z (the fourth argument)
        of the interpolated function at the given input.
        
        Parameters
        ----------
        w : np.array or float
            Real values to be evaluated in the interpolated function.
        x : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        y : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        z : np.array or float
            Real values to be evaluated in the interpolated function; must be
            the same size as w.
        
        Returns
        -------
        dfdz : np.array or float
            The derivative with respect to z of the interpolated function eval-
            uated at w,x,y,z: dfdz = f_z(w,x,y,z), with the same shape as inputs.
        '''
        wa = np.asarray(w)
        xa = np.asarray(x)
        ya = np.asarray(y)
        za = np.asarray(z)
        return (self._derZ(wa.flatten(),xa.flatten(),ya.flatten(),za.flatten())).reshape(wa.shape)
        
    def _evaluate(self,w,x,y,z):
        '''
        Interpolated function evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()
        
    def _derW(self,w,x,y,z):
        '''
        Interpolated function w-derivative evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()
        
    def _derX(self,w,x,y,z):
        '''
        Interpolated function w-derivative evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()
        
    def _derY(self,w,x,y,z):
        '''
        Interpolated function w-derivative evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()
        
    def _derZ(self,w,x,y,z):
        '''
        Interpolated function w-derivative evaluator, to be defined in subclasses.
        '''
        raise NotImplementedError()
        
        
class ConstantFunction(HARKobject):
    '''
    A class for representing trivial functions that return the same real output for any input.  This
    is convenient for models where an object might be a (non-trivial) function, but in some variations
    that object is just a constant number.  Rather than needing to make a (Bi/Tri/Quad)-
    LinearInterpolation with trivial state grids and the same f_value in every entry, ConstantFunction
    allows the user to quickly make a constant/trivial function.  This comes up, e.g., in models
    with endogenous pricing of insurance contracts; a contract's premium might depend on some state
    variables of the individual, but in some variations the premium of a contract is just a number.
    '''
    convergence_criteria = ['value']
    
    def __init__(self,value):
        '''
        Make a new ConstantFunction object.
        
        Parameters
        ----------
        value : float
            The constant value that the function returns.
        
        Returns
        -------
        None
        '''
        self.value = float(value)
        
    def __call__(self,*args):
        '''
        Evaluate the constant function.  The first input must exist and should be an array.
        Returns an array of identical shape to args[0] (if it exists).
        '''
        if len(args) > 0: # If there is at least one argument, return appropriately sized array
            if _isscalar(args[0]):
                return self.value
            else:    
                shape = args[0].shape
                return self.value*np.ones(shape)
        else: # Otherwise, return a single instance of the constant value
            return self.value
        
    def derivative(self,*args):
        '''
        Evaluate the derivative of the function.  The first input must exist and should be an array.
        Returns an array of identical shape to args[0] (if it exists).  This is an array of zeros.
        '''
        if len(args) > 0:
            if _isscalar(args[0]):
                return 0.0
            else:
                shape = args[0].shape
                return np.zeros(shape)
        else:
            return 0.0
        
    # All other derivatives are also zero everywhere, so these methods just point to derivative    
    derivativeX = derivative
    derivativeY = derivative
    derivativeZ = derivative
    derivativeW = derivative
    derivativeXX= derivative
    
    
class LinearInterp(HARKinterpolator1D):
    '''
    A "from scratch" 1D linear interpolation class.  Allows for linear or decay
    extrapolation (approaching a limiting linear function from below).    
    '''
    distance_criteria = ['x_list','y_list']
    
    def __init__(self,x_list,y_list,intercept_limit=None,slope_limit=None,lower_extrap=False):
        '''
        The interpolation constructor to make a new linear spline interpolation.
        
        Parameters
        ----------
        x_list : np.array
            List of x values composing the grid.
        y_list : np.array
            List of y values, representing f(x) at the points in x_list.
        intercept_limit : float
            Intercept of limiting linear function.
        slope_limit : float
            Slope of limiting linear function.
        lower_extrap : boolean
            Indicator for whether lower extrapolation is allowed.  False means
            f(x) = NaN for x < min(x_list); True means linear extrapolation.
            
        Returns
        -------
        new instance of LinearInterp
            
        NOTE: When no input is given for the limiting linear function, linear
        extrapolation is used above the highest gridpoint.        
        '''
        # Make the basic linear spline interpolation
        self.x_list = np.array(x_list)
        self.y_list = np.array(y_list)
        self.lower_extrap = lower_extrap
        self.x_n = self.x_list.size
        
        # Make a decay extrapolation
        if intercept_limit is not None and slope_limit is not None:
            slope_at_top = (y_list[-1] - y_list[-2])/(x_list[-1] - x_list[-2])
            level_diff   = intercept_limit + slope_limit*x_list[-1] - y_list[-1]
            slope_diff   = slope_limit - slope_at_top
            
            self.decay_extrap_A  = level_diff
            self.decay_extrap_B  = -slope_diff/level_diff
            self.intercept_limit = intercept_limit
            self.slope_limit     = slope_limit
            self.decay_extrap    = True
        else:
            self.decay_extrap = False


    def _evalOrDer(self,x,_eval,_Der):
        '''
        Returns the level and/or first derivative of the function at each value in
        x.  Only called internally by HARKinterpolator1D.eval_and_der (etc).

        Parameters
        ----------
        x : scalar or np.array
            Set of points where we want to evlauate the interpolated function and/or its derivative..
        _eval : boolean
            Indicator for whether to evalute the level of the interpolated function.
        _Der : boolean
            Indicator for whether to evaluate the derivative of the interpolated function.
            
        Returns
        -------
        A list including the level and/or derivative of the interpolated function where requested.
        '''
        i      = np.maximum(np.searchsorted(self.x_list[:-1],x),1)
        alpha  = (x-self.x_list[i-1])/(self.x_list[i]-self.x_list[i-1])

        if _eval:
                y = (1.-alpha)*self.y_list[i-1] + alpha*self.y_list[i]
        if _Der:
                dydx = (self.y_list[i] - self.y_list[i-1])/(self.x_list[i] - self.x_list[i-1])

        if not self.lower_extrap:
            below_lower_bound = x < self.x_list[0]

            if _eval:
                y[below_lower_bound] = np.nan
            if _Der:           
                dydx[below_lower_bound] = np.nan
        
        if self.decay_extrap:
            above_upper_bound = x > self.x_list[-1]
            x_temp = x[above_upper_bound] - self.x_list[-1]

            if _eval:
                y[above_upper_bound] = self.intercept_limit + \
                                       self.slope_limit*x[above_upper_bound] - \
                                       self.decay_extrap_A*np.exp(-self.decay_extrap_B*x_temp)            
            if _Der:            
                dydx[above_upper_bound] = self.slope_limit + \
                                          self.decay_extrap_B*self.decay_extrap_A*\
                                          np.exp(-self.decay_extrap_B*x_temp)
        output = []
        if _eval:
            output += [y,]
        if _Der:
            output += [dydx,]

        return output
            
    def _evaluate(self,x,return_indices = False):
        '''
        Returns the level of the interpolated function at each value in x.  Only
        called internally by HARKinterpolator1D.__call__ (etc).
        '''
        return self._evalOrDer(x,True,False)[0]
        
    def _der(self,x):
        '''
        Returns the first derivative of the interpolated function at each value
        in x. Only called internally by HARKinterpolator1D.derivative (etc).
        '''
        return self._evalOrDer(x,False,True)[0]

    def _evalAndDer(self,x):
        '''
        Returns the level and first derivative of the function at each value in
        x.  Only called internally by HARKinterpolator1D.eval_and_der (etc).
        '''
        y,dydx = self._evalOrDer(x,True,True)

        return y,dydx
        

class CubicInterp(HARKinterpolator1D):
    '''
    An interpolating function using piecewise cubic splines.  Matches level and
    slope of 1D function at gridpoints, smoothly interpolating in between.
    Extrapolation above highest gridpoint approaches a limiting linear function
    if desired (linear extrapolation also enabled.)
    '''
    distance_criteria = ['x_list','y_list','dydx_list']
    
    def __init__(self,x_list,y_list,dydx_list,intercept_limit=None,slope_limit=None,lower_extrap=False):
        '''
        The interpolation constructor to make a new cubic spline interpolation.
        
        Parameters
        ----------
        x_list : np.array
            List of x values composing the grid.
        y_list : np.array
            List of y values, representing f(x) at the points in x_list.
        dydx_list : np.array
            List of dydx values, representing f'(x) at the points in x_list
        intercept_limit : float
            Intercept of limiting linear function.
        slope_limit : float
            Slope of limiting linear function.
        lower_extrap : boolean
            Indicator for whether lower extrapolation is allowed.  False means
            f(x) = NaN for x < min(x_list); True means linear extrapolation.
            
        Returns
        -------
        new instance of CubicInterp
            
        NOTE: When no input is given for the limiting linear function, linear
        extrapolation is used above the highest gridpoint.        
        '''
        self.x_list = np.asarray(x_list)
        self.y_list = np.asarray(y_list)
        self.dydx_list = np.asarray(dydx_list)
        self.n = len(x_list)
        
        # Define lower extrapolation as linear function (or just NaN)
        if lower_extrap:
            self.coeffs = [[y_list[0],dydx_list[0],0,0]]
        else:
            self.coeffs = [[np.nan,np.nan,np.nan,np.nan]]

        # Calculate interpolation coefficients on segments mapped to [0,1]
        for i in xrange(self.n-1):
           x0 = x_list[i]
           y0 = y_list[i]
           x1 = x_list[i+1]
           y1 = y_list[i+1]
           Span = x1 - x0
           dydx0 = dydx_list[i]*Span
           dydx1 = dydx_list[i+1]*Span
           
           temp = [y0, dydx0, 3*(y1 - y0) - 2*dydx0 - dydx1, 2*(y0 - y1) + dydx0 + dydx1];
           self.coeffs.append(temp)

        # Calculate extrapolation coefficients as a decay toward limiting function y = mx+b
        if slope_limit is None and intercept_limit is None:
            slope_limit = dydx_list[-1]
            intercept_limit = y_list[-1] - slope_limit*x_list[-1]
        gap = slope_limit*x1 + intercept_limit - y1
        slope = slope_limit - dydx_list[self.n-1]
        if (gap != 0) and (slope <= 0):
            temp = [intercept_limit, slope_limit, gap, slope/gap]
        elif slope > 0:
            temp = [intercept_limit, slope_limit, 0, 0] # fixing a problem when slope is positive
        else:
            temp = [intercept_limit, slope_limit, gap, 0]
        self.coeffs.append(temp)
        self.coeffs = np.array(self.coeffs)

    def _evaluate(self,x):
        '''
        Returns the level of the interpolated function at each value in x.  Only
        called internally by HARKinterpolator1D.__call__ (etc).
        '''
        if _isscalar(x):
            pos = np.searchsorted(self.x_list,x)
            if pos == 0:
                y = self.coeffs[0,0] + self.coeffs[0,1]*(x - self.x_list[0])
            elif (pos < self.n):
                alpha = (x - self.x_list[pos-1])/(self.x_list[pos] - self.x_list[pos-1])
                y = self.coeffs[pos,0] + alpha*(self.coeffs[pos,1] + alpha*(self.coeffs[pos,2] + alpha*self.coeffs[pos,3]))
            else:
                alpha = x - self.x_list[self.n-1]
                y = self.coeffs[pos,0] + x*self.coeffs[pos,1] - self.coeffs[pos,2]*np.exp(alpha*self.coeffs[pos,3])
        else:
            m = len(x)
            pos = np.searchsorted(self.x_list,x)
            y = np.zeros(m)
            if y.size > 0:
                out_bot   = pos == 0
                out_top   = pos == self.n
                in_bnds   = np.logical_not(np.logical_or(out_bot, out_top))
                
                # Do the "in bounds" evaluation points
                i = pos[in_bnds]
                coeffs_in = self.coeffs[i,:]
                alpha = (x[in_bnds] - self.x_list[i-1])/(self.x_list[i] - self.x_list[i-1])
                y[in_bnds] = coeffs_in[:,0] + alpha*(coeffs_in[:,1] + alpha*(coeffs_in[:,2] + alpha*coeffs_in[:,3]))
                
                # Do the "out of bounds" evaluation points
                y[out_bot] = self.coeffs[0,0] + self.coeffs[0,1]*(x[out_bot] - self.x_list[0])
                alpha = x[out_top] - self.x_list[self.n-1]
                y[out_top] = self.coeffs[self.n,0] + x[out_top]*self.coeffs[self.n,1] - self.coeffs[self.n,2]*np.exp(alpha*self.coeffs[self.n,3])                      
        return y

    def _der(self,x):
        '''
        Returns the first derivative of the interpolated function at each value
        in x. Only called internally by HARKinterpolator1D.derivative (etc).
        '''
        if _isscalar(x):
            pos = np.searchsorted(self.x_list,x)
            if pos == 0:
                dydx = self.coeffs[0,1]
            elif (pos < self.n):
                alpha = (x - self.x_list[pos-1])/(self.x_list[pos] - self.x_list[pos-1])
                dydx = (self.coeffs[pos,1] + alpha*(2*self.coeffs[pos,2] + alpha*3*self.coeffs[pos,3]))/(self.x_list[pos] - self.x_list[pos-1])
            else:
                alpha = x - self.x_list[self.n-1]
                dydx = self.coeffs[pos,1] - self.coeffs[pos,2]*self.coeffs[pos,3]*np.exp(alpha*self.coeffs[pos,3])
        else:
            m = len(x)
            pos = np.searchsorted(self.x_list,x)
            dydx = np.zeros(m)
            if dydx.size > 0:
                out_bot   = pos == 0
                out_top   = pos == self.n
                in_bnds   = np.logical_not(np.logical_or(out_bot, out_top))
                
                # Do the "in bounds" evaluation points
                i = pos[in_bnds]
                coeffs_in = self.coeffs[i,:]
                alpha = (x[in_bnds] - self.x_list[i-1])/(self.x_list[i] - self.x_list[i-1])
                dydx[in_bnds] = (coeffs_in[:,1] + alpha*(2*coeffs_in[:,2] + alpha*3*coeffs_in[:,3]))/(self.x_list[i] - self.x_list[i-1])
                
                # Do the "out of bounds" evaluation points
                dydx[out_bot] = self.coeffs[0,1]
                alpha = x[out_top] - self.x_list[self.n-1]
                dydx[out_top] = self.coeffs[self.n,1] - self.coeffs[self.n,2]*self.coeffs[self.n,3]*np.exp(alpha*self.coeffs[self.n,3])
        return dydx


    def _evalAndDer(self,x):
        '''
        Returns the level and first derivative of the function at each value in
        x.  Only called internally by HARKinterpolator1D.eval_and_der (etc).
        '''
        if _isscalar(x):
            pos = np.searchsorted(self.x_list,x)
            if pos == 0:
                y = self.coeffs[0,0] + self.coeffs[0,1]*(x - self.x_list[0])
                dydx = self.coeffs[0,1]
            elif (pos < self.n):
                alpha = (x - self.x_list[pos-1])/(self.x_list[pos] - self.x_list[pos-1])
                y = self.coeffs[pos,0] + alpha*(self.coeffs[pos,1] + alpha*(self.coeffs[pos,2] + alpha*self.coeffs[pos,3]))
                dydx = (self.coeffs[pos,1] + alpha*(2*self.coeffs[pos,2] + alpha*3*self.coeffs[pos,3]))/(self.x_list[pos] - self.x_list[pos-1])
            else:
                alpha = x - self.x_list[self.n-1]
                y = self.coeffs[pos,0] + x*self.coeffs[pos,1] - self.coeffs[pos,2]*np.exp(alpha*self.coeffs[pos,3])
                dydx = self.coeffs[pos,1] - self.coeffs[pos,2]*self.coeffs[pos,3]*np.exp(alpha*self.coeffs[pos,3])
        else:
            m = len(x)
            pos = np.searchsorted(self.x_list,x)
            y = np.zeros(m)
            dydx = np.zeros(m)
            if y.size > 0:
                out_bot   = pos == 0
                out_top   = pos == self.n
                in_bnds   = np.logical_not(np.logical_or(out_bot, out_top))
                
                # Do the "in bounds" evaluation points
                i = pos[in_bnds]
                coeffs_in = self.coeffs[i,:]
                alpha = (x[in_bnds] - self.x_list[i-1])/(self.x_list[i] - self.x_list[i-1])
                y[in_bnds] = coeffs_in[:,0] + alpha*(coeffs_in[:,1] + alpha*(coeffs_in[:,2] + alpha*coeffs_in[:,3]))
                dydx[in_bnds] = (coeffs_in[:,1] + alpha*(2*coeffs_in[:,2] + alpha*3*coeffs_in[:,3]))/(self.x_list[i] - self.x_list[i-1])
                
                # Do the "out of bounds" evaluation points
                y[out_bot] = self.coeffs[0,0] + self.coeffs[0,1]*(x[out_bot] - self.x_list[0])
                dydx[out_bot] = self.coeffs[0,1]
                alpha = x[out_top] - self.x_list[self.n-1]
                y[out_top] = self.coeffs[self.n,0] + x[out_top]*self.coeffs[self.n,1] - self.coeffs[self.n,2]*np.exp(alpha*self.coeffs[self.n,3])
                dydx[out_top] = self.coeffs[self.n,1] - self.coeffs[self.n,2]*self.coeffs[self.n,3]*np.exp(alpha*self.coeffs[self.n,3])
        return y, dydx
    
    
    
    
class LinearInterpDiscont(LinearInterp):
    '''
    A "from scratch" 1D linear interpolation class.  Allows for linear or decay
    extrapolation (approaching a limiting linear function from below).  Function
    is not necessarily continuous; user can specify both y_left and y_right.
    '''
    distance_criteria = ['x_list','coeffs']
    
    def __init__(self,x_list,y_left,y_right=None,intercept_limit=None,slope_limit=None,lower_extrap=False):
        '''
        The interpolation constructor to make a new linear spline interpolation.
        
        NOTE: When no input is given for the limiting linear function, linear
        extrapolation is used above the highest gridpoint.   
        
        Parameters
        ----------
        x_list : np.array
            List of x values composing the grid.
        y_left : np.array
            List of y values, representing f(x-) at the points in x_list.  If
            y_right is not specified, these are f(x) value (no discontinuities).
        y_right : np.array
            List of y values, representing f(x+) at the points in x_list.  If
            not specified, then are y_left is f(x+) values (no discontinuities).
        intercept_limit : float
            Intercept of limiting linear function.
        slope_limit : float
            Slope of limiting linear function.
        lower_extrap : boolean
            Indicator for whether lower extrapolation is allowed.  False means
            f(x) = NaN for x < min(x_list); True means linear extrapolation.
            
        Returns
        -------
        new instance of LinearInterpDisCont
        '''
        # Store basic attributes
        x_list = np.array(x_list)
        self.x_list = x_list
        self.lower_extrap = lower_extrap
        self.x_n = self.x_list.size
        if y_right is None:
            y_right = y_left
            y_left = np.array(y_left)
            y_right = np.array(y_right)
        
        # Calculate coefficients for each segment
        slopes = (y_left[1:] - y_right[0:-1])/(x_list[1:] - x_list[0:-1])
        intercepts = y_right[0:-1] - slopes*x_list[0:-1]
        self.coeffs = np.vstack((intercepts,slopes))
        
        # Make a decay extrapolation
        if intercept_limit is not None and slope_limit is not None:
            slope_at_top = (y_left[-1] - y_right[-2])/(x_list[-1] - x_list[-2])
            level_diff   = intercept_limit + slope_limit*x_list[-1] - y_left[-1]
            slope_diff   = slope_limit - slope_at_top
            
            self.decay_extrap_A  = level_diff
            self.decay_extrap_B  = -slope_diff/level_diff
            self.intercept_limit = intercept_limit
            self.slope_limit     = slope_limit
            self.decay_extrap    = True
        else:
            self.decay_extrap = False


    def _evalOrDer(self,x,_eval,_Der):
        '''
        Returns the level and/or first derivative of the function at each value in
        x.  Only called internally by HARKinterpolator1D.eval_and_der (etc).

        Parameters
        ----------
        x : scalar or np.array
            Set of points where we want to evlauate the interpolated function and/or its derivative..
        _eval : boolean
            Indicator for whether to evalute the level of the interpolated function.
        _Der : boolean
            Indicator for whether to evaluate the derivative of the interpolated function.
            
        Returns
        -------
        A list including the level and/or derivative of the interpolated function where requested.
        '''
        i      = np.searchsorted(self.x_list[:-1],x,side='right') - 1
        
        slopes = self.coeffs[1,i]
        if _eval:
                y = self.coeffs[0,i] + slopes*x
        if _Der:
                dydx = slopes

        if not self.lower_extrap:
            below_lower_bound = x < self.x_list[0]

            if _eval:
                y[below_lower_bound] = np.nan
            if _Der:           
                dydx[below_lower_bound] = np.nan
        
        if self.decay_extrap:
            above_upper_bound = x > self.x_list[-1]
            x_temp = x[above_upper_bound] - self.x_list[-1]

            if _eval:
                y[above_upper_bound] = self.intercept_limit + \
                                       self.slope_limit*x[above_upper_bound] - \
                                       self.decay_extrap_A*np.exp(-self.decay_extrap_B*x_temp)            
            if _Der:            
                dydx[above_upper_bound] = self.slope_limit + \
                                          self.decay_extrap_B*self.decay_extrap_A*\
                                          np.exp(-self.decay_extrap_B*x_temp)
        output = []
        if _eval:
            output += [y,]
        if _Der:
            output += [dydx,]

        return output

    
    
class CubicInterpDiscont(CubicInterp):
    '''
    An interpolating function using piecewise cubic splines.  User supplies left
    and right value and derivative at each gridpoint, which may or may not be
    the same.  That is, discontinuities in level or derivative are permitted.
    Extrapolation above highest gridpoint approaches a limiting linear function
    if desired (linear extrapolation also enabled.)
    '''
    distance_criteria = ['x_list','coeffs']
    
    def __init__(self,x_list,y_left,y_right,dydx_left,dydx_right,intercept_limit=None,slope_limit=None,lower_extrap=False):
        '''
        The interpolation constructor to make a new cubic spline interpolation.
        
        Parameters
        ----------
        x_list : np.array
            List of x values composing the grid.
        y_left : np.array
            List of y values, representing f(x-) at the points in x_list.
        y_right : np.array
            List of y values, representing f(x+) at the points in x_list.
        dydx_left : np.array
            List of dydx values, representing f'(x-) at the points in x_list.
        dydx_right : np.array
            List of dydx values, representing f'(x+) at the points in x_list.
        intercept_limit : float
            Intercept of limiting linear function.
        slope_limit : float
            Slope of limiting linear function.
        lower_extrap : boolean
            Indicator for whether lower extrapolation is allowed.  False means
            f(x) = NaN for x < min(x_list); True means linear extrapolation.
            
        Returns
        -------
        new instance of CubicInterp
            
        NOTE: When no input is given for the limiting linear function, linear
        extrapolation is used above the highest gridpoint.        
        '''
        self.x_list = np.asarray(x_list)
        self.y_left = np.asarray(y_left)
        self.dydx_left = np.asarray(dydx_left)
        self.y_right = np.asarray(y_right)
        self.dydx_right = np.asarray(dydx_right)
        self.n = len(x_list)
        
        # Define lower extrapolation as linear function (or just NaN)
        if lower_extrap:
            self.coeffs = [[y_left[0],dydx_left[0],0,0]]
        else:
            self.coeffs = [[np.nan,np.nan,np.nan,np.nan]]

        # Calculate interpolation coefficients on segments mapped to [0,1]
        for i in xrange(self.n-1):
           x0 = x_list[i]
           y0 = y_right[i]
           x1 = x_list[i+1]
           y1 = y_left[i+1]
           Span = x1 - x0
           dydx0 = dydx_right[i]*Span
           dydx1 = dydx_left[i+1]*Span
           
           temp = [y0, dydx0, 3*(y1 - y0) - 2*dydx0 - dydx1, 2*(y0 - y1) + dydx0 + dydx1];
           self.coeffs.append(temp)

        # Calculate extrapolation coefficients as a decay toward limiting function y = mx+b
        if slope_limit is None and intercept_limit is None:
            slope_limit = dydx_right[-1]
            intercept_limit = y_right[-1] - slope_limit*x_list[-1]
        gap = slope_limit*x1 + intercept_limit - y1
        slope = slope_limit - dydx_right[self.n-1]
        if (gap != 0) and (slope <= 0):
            temp = [intercept_limit, slope_limit, gap, slope/gap]
        elif slope > 0:
            temp = [intercept_limit, slope_limit, 0, 0] # fixing a problem when slope is positive
        else:
            temp = [intercept_limit, slope_limit, gap, 0]
        self.coeffs.append(temp)
        self.coeffs = np.array(self.coeffs)



def evalTwoPointLine(x0,x1,y0,y1,x_query):
    '''
    Quick function for evaluating a linear function as defined by two points.
    Called repeatedly in FellaInterp.addNewPoints().  Either the y values or
    query points can be array, but not both.
    
    Parameters
    ----------
    x0 : float
        First point x value.
    x1 : float
        Second point x value.
    y0 : float or np.array
        First point y = f(x) value(s).
    y1 : float or np.array
        Second point y = f(x) value(s).
    x_query : float or np.array
        x values to be evaluated along the line.
        
    Returns
    -------
    out : float or np.array
    '''
    alpha = (x_query-x0)/(x1-x0)
    out = (1.-alpha)*y0 + alpha*y1
    return out
    
    
    
def solveTwoPointLines(x0,x1,y0,y1,x2,x3,y2,y3):
    '''
    Quick function for finding the intersection of two lines, each of which is
    defined by two points.  Called repeatedly by FellaInterp.addNewPoints().
    
    Parameters
    ----------
    x0 : float
        First point of first line x value.
    x1 : float
        Second point of first line x value.
    y0 : float
        First point of first line y = f(x) value.
    y1 : float
        Second point of first line y = f(x) value.
    x2 : float
        First point of second line x value.
    x3 : float
        Second point of second line x value.
    y2 : float
        First point of second line y = f(x) value.
    y3 : float
        Second point of second line y = f(x) value.
        
    Returns
    -------
    x : float
        Intersection of two lines in x.
    y : float
        Intersection of two lines in y = f(x).
    '''
    denom = ((x0 - x1)*(y2 - y3) - (y0 - y1)*(x2 - x3))
    A = (x0*y1 - x1*y0)
    B = (x2*y3 - x3*y2)
    x = (A*(x2 - x3) - (x0 - x1)*B)/denom
    y = (A*(y2 - y3) - (y0 - y1)*B)/denom
    return x, y
        
        
        
class FellaInterp(HARKobject):
    '''
    A 1D interpolator that implements  a variation on Giulio Fella's "upper envelope" method.
    Fella presents a method for applying the endogenous grid method with non-concave value.
    Ordinarily, this would create an issue when the optimal policy implied by the first order
    condition "doubles back" on itself near the non-concavity.  Fella's method generates the
    correct policy function by taking the upper envelope of the value function when multiple
    solutions to the FOC are found for one state.
    
    Stated differently, generic EGM generates an approximation to the set of states and
    controls that satisfy the first order condition(s), with accompanying continuation values.
    In many models (like ConsIndShock), there is exactly one control that satisfies the FOC
    at each state in the state space, so generic EGM generates the true policy and value
    functions, with no additional work.  However, in the presence of non-concave future value,
    discrete choice, and/or discontinuities in the utility or transition functions, the set
    of FOC-satisfying points might have multiple controls at a particular state; the *true*
    policy at this state is the control associated with the highest continuation value.
    
    This class initializes with a constant value and policy function, and is subsequently
    "improved" by passing sequences of candidate states-values-policies (assumed to be 
    linearly continuous) and selecting the best candidate policy at each state, constructing
    a new value and policy function.  The constructed policy function may be discontinuous,
    and the constructed value function may be non-concave.
    '''
    distance_criteria = ['PolicyFunc']

    def __init__(self, v0=-np.inf, control0=0.0, lower_bound=None, upper_bound=None):
        '''
        Make a new FellaInterp instance.  It will initially have a constant value
        function and constant policy functions; these will be improved by calls to
        the method addNewPoints.
        
        Parameters
        ----------
        v0 : float
            Initial value for the Fella value function, constant across all states.
        control0 : float or [float]
            Initial control levels, constant across all states; can be a single float or a list of floats.
        lower_bound : float or None
            Lower bound of the state variable (domain),  if any.
        upper_bound : float or None
            Initial upper bound of the state variable (domain), if any.
        '''
        if lower_bound is None:
            bot = 0.0
        else:
            bot = lower_bound
        if upper_bound is None:
            top = bot + 1000000.
        else:
            top = upper_bound
        
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.value_grid = np.array([v0,v0])
        self.state_grid = np.array([bot,top])
        if type(control0) is not list:
            policy_count = 1
        else:
            policy_count = len(control0)
        self.left_policy = np.zeros((policy_count,2))
        self.right_policy = np.zeros((policy_count,2))
        self.left_policy[:,0] = control0
        self.right_policy[:,0] = control0
        self.left_policy[:,1] = control0
        self.right_policy[:,1] = control0
        
            
    def addNewPoints(self,states,values,policies,extrapolate):
        '''
        Update the Fella functions with new candidate points.  Each input is an
        array of the same length; corresponding elements across arrays represent
        a candidate (state,value,policy).  This method incorporates these new
        points into the "upper envelope" of the current value function, generating
        potentially discontinuous policy functions.
        
        Parameters
        ----------
        states : np.array
            1D array of states for the candidate points.
        values : np.array
            1D array of values associated with each of the candidate states.
        policies : np.array
            1D or 2D array of control variables at the candidate states; different
            control variables are stored in different rows of policies.
        extrapolate : bool
            Indicator for whether the last linear segment of the candidate should
            be extrapolated indefinitely outward.
        '''
        if len(policies.shape) == 1:
            policies = np.reshape(policies,(1,policies.size))
        N = policies.shape[0]
        
        # Initialize direction so that first "switch check" passes and initialize empty replacement point objects
        moving_right = (states[1] > states[0]) # Hopefully always True
        value_new = np.zeros(0)
        state_new = np.zeros(0)
        left_policy_new  = np.zeros((N,0))
        right_policy_new = np.zeros((N,0))
        K = 0
        
        # Loop over the segments in the candidate set
        for j in range(states.size-1):
            skip_start = False
            
            # Check whether direction has changed; if so, insert replacement points now
            new_dir = (states[j+1] > states[j])
            if (new_dir != moving_right) and (state_new.size > 0):
                # Add "turning point" if it dominates
                i = np.searchsorted(self.state_grid,states[j])
                v_temp = evalTwoPointLine(self.state_grid[i-1],self.state_grid[i],self.value_grid[i-1],self.value_grid[i],states[j])
                if (values[j] > v_temp):
                    orig_policies = np.reshape(evalTwoPointLine(self.state_grid[i-1],self.state_grid[i],self.right_policy[:,i-1],self.left_policy[:,i],states[j]),(N,1))
                    if moving_right:
                        i = -1
                    else:
                        i = 0
                    value_new = np.insert(value_new,i,values[j])
                    state_new = np.insert(state_new,i,states[j])
                    if moving_right:
                        left_policy_new = np.insert(left_policy_new,[i],np.reshape(policies[:,j],(N,1)),axis=1)
                        right_policy_new = np.insert(right_policy_new,[i],np.reshape(orig_policies,(N,1)),axis=1)
                    else:
                        right_policy_new = np.insert(right_policy_new,[i],np.reshape(policies[:,j],(N,1)),axis=1)
                        left_policy_new = np.insert(left_policy_new,[i],np.reshape(orig_policies,(N,1)),axis=1)
                    candidate_better = True
                    skip_start = True
                               
                # Delete points inside span of replacement points
                bot = np.searchsorted(self.state_grid,state_new[0])
                top = np.searchsorted(self.state_grid,state_new[-1])
                self.state_grid = np.delete(self.state_grid,np.arange(bot,top))
                self.value_grid = np.delete(self.value_grid,np.arange(bot,top))
                self.left_policy  = np.delete(self.left_policy, np.arange(bot,top),axis=1)
                self.right_policy = np.delete(self.right_policy,np.arange(bot,top),axis=1)
                
                # Add new points to self
                self.state_grid = np.insert(self.state_grid,bot,state_new)
                self.value_grid = np.insert(self.value_grid,bot,value_new)
                self.left_policy = np.insert(self.left_policy,[bot],left_policy_new,axis=1)
                self.right_policy = np.insert(self.right_policy,[bot],right_policy_new,axis=1)
                
                # Reset the replacement points objects
                value_new = np.zeros(0)
                state_new = np.zeros(0)
                left_policy_new  = np.zeros((N,0))
                right_policy_new = np.zeros((N,0))
                K = 0
                
            # Get bounds of this segment with respect to existing state grid   
            moving_right = new_dir    
            start_idx = np.searchsorted(self.state_grid,states[j])
            end_idx = np.searchsorted(self.state_grid,states[j+1])

            # Determine index bounds for this segment and make the set of original indices to loop over
            if moving_right:
                bot = start_idx
                if j == (states.size-2): # If this is the last candidate segment,
                    top = self.state_grid.size # take all remaining original points
                else:
                    top = end_idx
                idx_set = np.arange(bot,top)
                i = bot
                a = 1 # incrementer
            else:
                bot = end_idx
                top = start_idx
                idx_set = np.arange(top-1,bot-1,-1)
                i = top
                a = -1 # incrementer
                
            # Determine whether candidate or original value is higher at each point
            state_temp = self.state_grid[bot:top]
            v_orig = self.value_grid[bot:top]
            v_cand = evalTwoPointLine(states[j],states[j+1],values[j],values[j+1],state_temp)
            dominance = v_cand > v_orig
            if not moving_right:
                dominance = np.flip(dominance,axis=0)
                        
            # Add the starting point of the segment to replacement points if it dominates original
            # Also add starting point if starting point is above highest gridpoint
            v_temp = evalTwoPointLine(self.state_grid[i-1],self.state_grid[i],self.value_grid[i-1],self.value_grid[i],states[j])
            if ((values[j] > v_temp) or (start_idx == self.state_grid.size)) and (not skip_start):
                z = moving_right*K # 0 if moving left, K if moving right
                orig_policies = evalTwoPointLine(self.state_grid[i-1],self.state_grid[i],self.right_policy[:,i-1],self.left_policy[:,i],states[j])
                value_new = np.insert(value_new,z,values[j])
                state_new = np.insert(state_new,z,states[j])
                left_policy_new = np.insert(left_policy_new,[z],np.reshape(policies[:,j],(N,1)),axis=1)
                right_policy_new = np.insert(right_policy_new,[z],np.reshape(policies[:,j],(N,1)),axis=1)
                if j == 0: # If this is the very first candidate point AND it dominates...
                    if moving_right:
                        left_policy_new[:,0] = orig_policies
                    else:
                        right_policy_new[:,0] = orig_policies
                candidate_better = True
                K += 1
            else:
                candidate_better = False
            
            # Loop over the index set to fill in the set of replacement points
            for k in range(idx_set.size):
                i = idx_set[k]
                # If dominance switches, add a point at value crossing
                if dominance[k] != candidate_better: 
                    cross_state, cross_value = solveTwoPointLines(states[j],states[j+1],values[j],values[j+1],self.state_grid[i-a],self.state_grid[i],self.value_grid[i-a],self.value_grid[i])
                    cand_policies = np.reshape(evalTwoPointLine(states[j],states[j+1],policies[:,j],policies[:,j+1],cross_state),(N,1))
                    orig_policies = np.reshape(evalTwoPointLine(self.state_grid[i-a],self.state_grid[i],self.right_policy[:,i-a],self.left_policy[:,i],cross_state),(N,1))
                    z = moving_right*K # 0 if moving left, K if moving right
                    state_new = np.insert(state_new,z,cross_state)
                    value_new = np.insert(value_new,z,cross_value)
                    if candidate_better == moving_right: # Candidate goes on left, original goes on right
                        left_policy_new  = np.insert(left_policy_new,[z],cand_policies,axis=1)
                        right_policy_new = np.insert(right_policy_new,[z],orig_policies,axis=1)
                    else:                                # Original goes on left, candidate goes on right
                        left_policy_new  = np.insert(left_policy_new,[z],orig_policies,axis=1)
                        right_policy_new = np.insert(right_policy_new,[z],cand_policies,axis=1)
                    K += 1
                
                # If original dominates, add it to our replacement set
                if not dominance[k]:
                    z = moving_right*K # 0 if moving left, K if moving right
                    state_new = np.insert(state_new,z,self.state_grid[i])
                    value_new = np.insert(value_new,z,self.value_grid[i])
                    left_policy_new  = np.insert(left_policy_new,[z],np.reshape(self.left_policy[:,i],(N,1)),axis=1)
                    right_policy_new = np.insert(right_policy_new,[z],np.reshape(self.right_policy[:,i],(N,1)),axis=1)
                    K += 1
                    
                candidate_better = dominance[k]
                    
            # Check for dominance switching between last original state and end point of segment
            i = end_idx
            v_orig = evalTwoPointLine(self.state_grid[i-1],self.state_grid[i],self.value_grid[i-1],self.value_grid[i],states[j+1])
            end_dom = values[j+1] > v_orig
            if (end_dom != candidate_better) and (j < states.size-2):
                cross_state, cross_value = solveTwoPointLines(states[j],states[j+1],values[j],values[j+1],self.state_grid[i-1],self.state_grid[i],self.value_grid[i-1],self.value_grid[i])
                cand_policies = np.reshape(evalTwoPointLine(states[j],states[j+1],policies[:,j],policies[:,j+1],cross_state),(N,1))
                orig_policies = np.reshape(evalTwoPointLine(self.state_grid[i-1],self.state_grid[i],self.right_policy[:,i-1],self.left_policy[:,i],cross_state),(N,1))
                z = moving_right*K # 0 if moving left, K if moving right
                state_new = np.insert(state_new,z,cross_state)
                value_new = np.insert(value_new,z,cross_value)
                if candidate_better == moving_right: # Candidate goes on left, original goes on right
                    left_policy_new  = np.insert(left_policy_new,[z],cand_policies,axis=1)
                    right_policy_new = np.insert(right_policy_new,[z],orig_policies,axis=1)
                else:                                # Original goes on left, candidate goes on right
                    left_policy_new  = np.insert(left_policy_new,[z],orig_policies,axis=1)
                    right_policy_new = np.insert(right_policy_new,[z],cand_policies,axis=1)
                K += 1
                candidate_better = end_dom

            # If this is the last segment *and* the end point dominates the original, add it to the set
            if j == (states.size-2):
                i = np.minimum(np.searchsorted(self.state_grid,states[-1]),self.state_grid.size-1)
                v_orig = evalTwoPointLine(self.state_grid[i-1],self.state_grid[i],self.value_grid[i-1],self.value_grid[i],states[-1])
                orig_policies = evalTwoPointLine(self.state_grid[i-1],self.state_grid[i],self.right_policy[:,i-1],self.left_policy[:,i],states[-1])
                if (values[-1] > v_orig) or (states[-1] > self.state_grid[-1]):
                    try:
                        z = np.searchsorted(state_new,states[-1]) # usually 0 if moving left, K if moving right, but possibly elsewhere in a weird case
                    except:
                        z = 0
                    state_new = np.insert(state_new,z,states[-1])
                    value_new = np.insert(value_new,z,values[-1])
                    left_policy_new = np.insert(left_policy_new,[z],np.reshape(policies[:,-1],(N,1)),axis=1)
                    right_policy_new = np.insert(right_policy_new,[z],np.reshape(policies[:,-1],(N,1)),axis=1)
                    if not moving_right:
                        left_policy_new[:,z] = orig_policies
                    elif (z == state_new.size-1) and not extrapolate:
                        right_policy_new[:,z] = orig_policies
                    K += 1
            
        # Looping over candidate segments is done, add last batch of replacement points
        if state_new.size > 0:
            bot = np.searchsorted(self.state_grid,state_new[0])
            if moving_right:
                top = self.state_grid.size # Go all the way to the end
            else:
                top = np.searchsorted(self.state_grid,state_new[-1])
            self.state_grid = np.delete(self.state_grid,np.arange(bot,top))
            self.value_grid = np.delete(self.value_grid,np.arange(bot,top))
            self.left_policy  = np.delete(self.left_policy, np.arange(bot,top),axis=1)
            self.right_policy = np.delete(self.right_policy,np.arange(bot,top),axis=1)
            self.state_grid = np.insert(self.state_grid,bot,state_new)
            self.value_grid = np.insert(self.value_grid,bot,value_new)
            self.left_policy = np.insert(self.left_policy,[bot],left_policy_new,axis=1)
            self.right_policy = np.insert(self.right_policy,[bot],right_policy_new,axis=1)
            
        # Deal with upper extrapolation if requested
        if extrapolate and moving_right:
            if (self.state_grid[-1] == states[-1]) and (self.value_grid[-1] == values[-1]):
                # Highest gridpoint is the last candidate gridpoint, so extrapolate it
                self.right_policy[:,-1] = self.left_policy[:,-1]
                value_slope = (self.value_grid[-1] - self.value_grid[-2])/(self.state_grid[-1] - self.state_grid[-2])
                policy_slope = (self.left_policy[:,-1] - self.right_policy[:,-2])/(self.state_grid[-1] - self.state_grid[-2])
                big_jump = 1000000.
                self.state_grid = np.append(self.state_grid,self.state_grid[-1] + big_jump)
                self.value_grid = np.append(self.value_grid,self.value_grid[-1] + big_jump*value_slope)
                temp = self.right_policy[:,-1] + big_jump*policy_slope
                self.left_policy = np.append(self.left_policy,np.reshape(temp,(N,1)),axis=1)
                self.right_policy = np.append(self.right_policy,np.reshape(temp,(N,1)),axis=1)
            elif not candidate_better:
                # If top gridpoint is not last candidate gridpoint, check whether last candidate segment *eventually* crosses current version
                cross_state, cross_value = solveTwoPointLines(states[-2],states[-1],values[-2],values[-1],self.state_grid[-2],self.state_grid[-1],self.value_grid[-2],self.value_grid[-1])
                if (cross_state > self.state_grid[-1]): # Add crossing point if it's past last gridpoint
                    orig_policies = np.reshape(evalTwoPointLine(self.state_grid[-2],self.state_grid[-1],self.right_policy[:,-2],self.left_policy[:,-1],cross_state),(N,1))
                    cand_policies = np.reshape(evalTwoPointLine(states[-2],states[-1],policies[:,-2],policies[:,-1],cross_state),(N,1))
                    self.state_grid = np.append(self.state_grid,cross_state)
                    self.value_grid = np.append(self.value_grid,cross_value)
                    self.left_policy = np.append(self.left_policy,orig_policies,axis=1)
                    self.right_policy = np.append(self.right_policy,cand_policies,axis=1)
                    
                    # Then add extrapolation point
                    value_slope = (values[-1] - values[-2])/(states[-1] - states[-2])
                    policy_slope = (policies[:,-1] - policies[:,-2])/(states[-1] - states[-2])
                    big_jump = 1000000.
                    self.state_grid = np.append(self.state_grid,self.state_grid[-1] + big_jump)
                    self.value_grid = np.append(self.value_grid,self.value_grid[-1] + big_jump*value_slope)
                    self.left_policy = np.append(self.left_policy,np.reshape(self.right_policy[:,-1] + big_jump*policy_slope,(N,1)),axis=1)
                    self.right_policy = np.append(self.right_policy,np.reshape(self.right_policy[:,-1] + big_jump*policy_slope,(N,1)),axis=1)
            else: # Only get here if candidate func overtakes original func beyond highest new point
                # Then add extrapolation point
                value_slope = (values[-1] - values[-2])/(states[-1] - states[-2])
                policy_slope = (policies[:,-1] - policies[:,-2])/(states[-1] - states[-2])
                big_jump = 1000000.
                self.state_grid = np.append(self.state_grid,self.state_grid[-1] + big_jump)
                self.value_grid = np.append(self.value_grid,self.value_grid[-1] + big_jump*value_slope)
                self.left_policy = np.append(self.left_policy,np.reshape(self.right_policy[:,-1] + big_jump*policy_slope,(N,1)),axis=1)
                self.right_policy = np.append(self.right_policy,np.reshape(self.right_policy[:,-1] + big_jump*policy_slope,(N,1)),axis=1)
        
                    
    def makeValueAndPolicyFuncs(self,intercept_limit=None,slope_limit=None):
        '''
        Make a value function and policy functions based on the current grids.
        Uses the attributes state_grid, value_grid, left_policy, right_policy to
        construct value and policy functions; these were created by one or more
        calls to addNewPoints().  Makes attributes ValueFunc and PolicyFuncs.
        
        Needs to be fixed to handle decay extrapolation.
        
        Parameters
        ----------
        intercept_limit : float, [float], or None
            Intercept(s) of limiting linear policy function(s), for decay extrapolation.
            Optional, defaults to None (linear extrapolation).
        slope_limit : float, [float], or None
            Slope(s) of limiting linear policy functions, for decay extrapolation.
            Optional, defaults to None (linear extrapolation).
            
        Returns
        -------
        None
        '''
        self.ValueFunc = LinearInterp(self.state_grid,self.value_grid)
        
        N = self.left_policy.shape[0]
        if intercept_limit is None:
            intercept_limit = [None]*N
        if slope_limit is None:
            slope_limit = [None]*N
        
        PolicyFuncs = []
        for n in range(N):
            PolicyFuncs.append(LinearInterpDiscont(self.state_grid,self.left_policy[n,:],self.right_policy[n,:],
                                                   intercept_limit=intercept_limit[n], slope_limit = slope_limit[n]))
        self.PolicyFuncs = PolicyFuncs
        
        
    def makeCRRAvNvrsFunc(self,CRRA,MPCmax,MPCmin,vPnvrsIdx):
        '''
        Make a pseudo-inverse CRRA value function compatible with ConsIndShockModel.ValueFunc.
        The ValueFunc attribute will be a CubicInterpDiscount that is continuous
        but non-smooth.  Pseudo-inverse marginal value function index must be given.
        value_grid is assumed to be in pseudo-inverse form.
        
        Needs to be improved to fix extrapolation and slope at bottom.
        
        Parameters
        ----------
        CRRA : float
            Coefficient of relative risk aversion.
        MPCmax : float
            Effective MPC as resources approach lower bound.
        MPCmin : float
            Effective MPC as resources go to infinity.
        vPnvrsIdx : int
            Index for the pseudo-inverse marginal value function in attributes
            left_policy and right_policy.
            
        Returns
        -------
        None
        '''
        u = lambda c : CRRAutility(c,gam=CRRA)
        uP = lambda c : CRRAutilityP(c,gam=CRRA)
        uinvP = lambda x : CRRAutility_invP(x,gam=CRRA)
        
        vNvrs = self.value_grid
        if (vNvrs[0] == 0.) and (CRRA >= 1.):
            bot_fix = True # numpy generates obnoxious warnings when value goes to -inf at bottom
            these = np.arange(1,vNvrs.size,dtype=int)
        else:
            bot_fix = False
            these = np.arange(vNvrs.size,dtype=int)
        v = u(vNvrs[these])
        vP_left = uP(self.left_policy[vPnvrsIdx,these])
        vP_right = uP(self.right_policy[vPnvrsIdx,these])
        
        temp = uinvP(v)
        vNvrsP_left = vP_left*temp
        vNvrsP_right = vP_right*temp
        if bot_fix: # If bottom point was removed, add it back on...
            vNvrsP_left = np.insert(vNvrsP_left,0,MPCmax**(-CRRA/(1.-CRRA)))
            vNvrsP_right = np.insert(vNvrsP_right,0,vNvrsP_left[0])
        else: # ...or just fix pseudo-inverse marg value at bottom
            vNvrsP_left[0] = MPCmax**(-CRRA/(1.-CRRA))
            vNvrsP_right[0] = vNvrsP_left[0]
        MPCminNvrs = MPCmin**(-CRRA/(1.0-CRRA))
        vNvrsFunc = CubicInterpDiscont(self.state_grid,vNvrs,vNvrs,vNvrsP_left,vNvrsP_right,0.0,MPCminNvrs)
        self.ValueFunc = vNvrsFunc
                
            
        
class BilinearInterp(HARKinterpolator2D):
    '''
    Bilinear full (or tensor) grid interpolation of a function f(x,y).
    '''
    distance_criteria = ['x_list','y_list','f_values']

    def __init__(self,f_values,x_list,y_list,xSearchFunc=None,ySearchFunc=None):
        '''
        Constructor to make a new bilinear interpolation.
        
        Parameters
        ----------
        f_values : numpy.array
            An array of size (x_n,y_n) such that f_values[i,j] = f(x_list[i],y_list[j])
        x_list : numpy.array
            An array of x values, with length designated x_n.
        y_list : numpy.array
            An array of y values, with length designated y_n.
        xSearchFunc : function
            An optional function that returns the reference location for x values:
            indices = xSearchFunc(x_list,x).  Default is np.searchsorted
        ySearchFunc : function
            An optional function that returns the reference location for y values:
            indices = ySearchFunc(y_list,y).  Default is np.searchsorted
            
        Returns
        -------
        new instance of BilinearInterp
        '''
        self.f_values = f_values
        self.x_list = x_list
        self.y_list = y_list
        self.x_n = x_list.size
        self.y_n = y_list.size
        if xSearchFunc is None:
            xSearchFunc = np.searchsorted
        if ySearchFunc is None:
            ySearchFunc = np.searchsorted
        self.xSearchFunc = xSearchFunc
        self.ySearchFunc = ySearchFunc
        
    def _evaluate(self,x,y):
        '''
        Returns the level of the interpolated function at each value in x,y.
        Only called internally by HARKinterpolator2D.__call__ (etc).
        '''
        if _isscalar(x):
            x_pos = max(min(self.xSearchFunc(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(self.ySearchFunc(self.y_list,y),self.y_n-1),1)
        else:
            x_pos = self.xSearchFunc(self.x_list,x)
            x_pos[x_pos < 1] = 1
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = self.ySearchFunc(self.y_list,y)
            y_pos[y_pos < 1] = 1
            y_pos[y_pos > self.y_n-1] = self.y_n-1
        alpha = (x - self.x_list[x_pos-1])/(self.x_list[x_pos] - self.x_list[x_pos-1])
        beta = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
        f = (
             (1-alpha)*(1-beta)*self.f_values[x_pos-1,y_pos-1]
          +  (1-alpha)*beta*self.f_values[x_pos-1,y_pos]
          +  alpha*(1-beta)*self.f_values[x_pos,y_pos-1]
          +  alpha*beta*self.f_values[x_pos,y_pos])
        return f
        
    def _derX(self,x,y):
        '''
        Returns the derivative with respect to x of the interpolated function
        at each value in x,y. Only called internally by HARKinterpolator2D.derivativeX.
        '''
        if _isscalar(x):
            x_pos = max(min(self.xSearchFunc(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(self.ySearchFunc(self.y_list,y),self.y_n-1),1)
        else:
            x_pos = self.xSearchFunc(self.x_list,x)
            x_pos[x_pos < 1] = 1
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = self.ySearchFunc(self.y_list,y)
            y_pos[y_pos < 1] = 1
            y_pos[y_pos > self.y_n-1] = self.y_n-1
        beta = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
        dfdx = (
              ((1-beta)*self.f_values[x_pos,y_pos-1]
            +  beta*self.f_values[x_pos,y_pos]) -
              ((1-beta)*self.f_values[x_pos-1,y_pos-1]
            +  beta*self.f_values[x_pos-1,y_pos]))/(self.x_list[x_pos] - self.x_list[x_pos-1])
        return dfdx
        
    def _derY(self,x,y):
        '''
        Returns the derivative with respect to y of the interpolated function
        at each value in x,y. Only called internally by HARKinterpolator2D.derivativeY.
        '''
        if _isscalar(x):
            x_pos = max(min(self.xSearchFunc(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(self.ySearchFunc(self.y_list,y),self.y_n-1),1)
        else:
            x_pos = self.xSearchFunc(self.x_list,x)
            x_pos[x_pos < 1] = 1
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = self.ySearchFunc(self.y_list,y)
            y_pos[y_pos < 1] = 1
            y_pos[y_pos > self.y_n-1] = self.y_n-1
        alpha = (x - self.x_list[x_pos-1])/(self.x_list[x_pos] - self.x_list[x_pos-1])
        dfdy = (
              ((1-alpha)*self.f_values[x_pos-1,y_pos]
            +  alpha*self.f_values[x_pos,y_pos]) -
              ((1-alpha)*self.f_values[x_pos-1,y_pos]
            +  alpha*self.f_values[x_pos-1,y_pos-1]))/(self.y_list[y_pos] - self.y_list[y_pos-1])
        return dfdy


class TrilinearInterp(HARKinterpolator3D):
    '''
    Trilinear full (or tensor) grid interpolation of a function f(x,y,z).
    '''
    distance_criteria = ['f_values','x_list','y_list','z_list']
    
    def __init__(self,f_values,x_list,y_list,z_list,xSearchFunc=None,ySearchFunc=None,zSearchFunc=None):
        '''
        Constructor to make a new trilinear interpolation.
        
        Parameters
        ----------
        f_values : numpy.array
            An array of size (x_n,y_n,z_n) such that f_values[i,j,k] =
            f(x_list[i],y_list[j],z_list[k])
        x_list : numpy.array
            An array of x values, with length designated x_n.
        y_list : numpy.array
            An array of y values, with length designated y_n.
        z_list : numpy.array
            An array of z values, with length designated z_n.
        xSearchFunc : function
            An optional function that returns the reference location for x values:
            indices = xSearchFunc(x_list,x).  Default is np.searchsorted
        ySearchFunc : function
            An optional function that returns the reference location for y values:
            indices = ySearchFunc(y_list,y).  Default is np.searchsorted
        zSearchFunc : function
            An optional function that returns the reference location for z values:
            indices = zSearchFunc(z_list,z).  Default is np.searchsorted
            
        Returns
        -------
        new instance of TrilinearInterp
        '''
        self.f_values = f_values
        self.x_list = x_list
        self.y_list = y_list
        self.z_list = z_list
        self.x_n = x_list.size
        self.y_n = y_list.size
        self.z_n = z_list.size
        if xSearchFunc is None:
            xSearchFunc = np.searchsorted
        if ySearchFunc is None:
            ySearchFunc = np.searchsorted
        if zSearchFunc is None:
            zSearchFunc = np.searchsorted
        self.xSearchFunc = xSearchFunc
        self.ySearchFunc = ySearchFunc
        self.zSearchFunc = zSearchFunc
        
    def _evaluate(self,x,y,z):
        '''
        Returns the level of the interpolated function at each value in x,y,z.
        Only called internally by HARKinterpolator3D.__call__ (etc).
        '''
        if _isscalar(x):
            x_pos = max(min(self.xSearchFunc(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(self.ySearchFunc(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(self.zSearchFunc(self.z_list,z),self.z_n-1),1)
        else:
            x_pos = self.xSearchFunc(self.x_list,x)
            x_pos[x_pos < 1] = 1
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = self.ySearchFunc(self.y_list,y)
            y_pos[y_pos < 1] = 1
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            z_pos = self.zSearchFunc(self.z_list,z)
            z_pos[z_pos < 1] = 1
            z_pos[z_pos > self.z_n-1] = self.z_n-1
        alpha = (x - self.x_list[x_pos-1])/(self.x_list[x_pos] - self.x_list[x_pos-1])
        beta = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
        gamma = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
        f = (
             (1-alpha)*(1-beta)*(1-gamma)*self.f_values[x_pos-1,y_pos-1,z_pos-1]
          +  (1-alpha)*(1-beta)*gamma*self.f_values[x_pos-1,y_pos-1,z_pos]
          +  (1-alpha)*beta*(1-gamma)*self.f_values[x_pos-1,y_pos,z_pos-1]
          +  (1-alpha)*beta*gamma*self.f_values[x_pos-1,y_pos,z_pos]
          +  alpha*(1-beta)*(1-gamma)*self.f_values[x_pos,y_pos-1,z_pos-1]
          +  alpha*(1-beta)*gamma*self.f_values[x_pos,y_pos-1,z_pos]
          +  alpha*beta*(1-gamma)*self.f_values[x_pos,y_pos,z_pos-1]
          +  alpha*beta*gamma*self.f_values[x_pos,y_pos,z_pos])
        return f
        
    def _derX(self,x,y,z):
        '''
        Returns the derivative with respect to x of the interpolated function
        at each value in x,y,z. Only called internally by HARKinterpolator3D.derivativeX.
        '''
        if _isscalar(x):
            x_pos = max(min(self.xSearchFunc(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(self.ySearchFunc(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(self.zSearchFunc(self.z_list,z),self.z_n-1),1)
        else:
            x_pos = self.xSearchFunc(self.x_list,x)
            x_pos[x_pos < 1] = 1
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = self.ySearchFunc(self.y_list,y)
            y_pos[y_pos < 1] = 1
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            z_pos = self.zSearchFunc(self.z_list,z)
            z_pos[z_pos < 1] = 1
            z_pos[z_pos > self.z_n-1] = self.z_n-1
        beta = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
        gamma = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
        dfdx = (
           (  (1-beta)*(1-gamma)*self.f_values[x_pos,y_pos-1,z_pos-1]
           +  (1-beta)*gamma*self.f_values[x_pos,y_pos-1,z_pos]
           +  beta*(1-gamma)*self.f_values[x_pos,y_pos,z_pos-1]
           +  beta*gamma*self.f_values[x_pos,y_pos,z_pos]) -
           (  (1-beta)*(1-gamma)*self.f_values[x_pos-1,y_pos-1,z_pos-1]
           +  (1-beta)*gamma*self.f_values[x_pos-1,y_pos-1,z_pos]
           +  beta*(1-gamma)*self.f_values[x_pos-1,y_pos,z_pos-1]
           +  beta*gamma*self.f_values[x_pos-1,y_pos,z_pos]))/(self.x_list[x_pos] - self.x_list[x_pos-1])
        return dfdx
        
    def _derY(self,x,y,z):
        '''
        Returns the derivative with respect to y of the interpolated function
        at each value in x,y,z. Only called internally by HARKinterpolator3D.derivativeY.
        '''
        if _isscalar(x):
            x_pos = max(min(self.xSearchFunc(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(self.ySearchFunc(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(self.zSearchFunc(self.z_list,z),self.z_n-1),1)
        else:
            x_pos = self.xSearchFunc(self.x_list,x)
            x_pos[x_pos < 1] = 1
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = self.ySearchFunc(self.y_list,y)
            y_pos[y_pos < 1] = 1
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            z_pos = self.zSearchFunc(self.z_list,z)
            z_pos[z_pos < 1] = 1
            z_pos[z_pos > self.z_n-1] = self.z_n-1
        alpha = (x - self.x_list[x_pos-1])/(self.x_list[x_pos] - self.x_list[x_pos-1])
        gamma = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
        dfdy = (
           (  (1-alpha)*(1-gamma)*self.f_values[x_pos-1,y_pos,z_pos-1]
           +  (1-alpha)*gamma*self.f_values[x_pos-1,y_pos,z_pos]
           +  alpha*(1-gamma)*self.f_values[x_pos,y_pos,z_pos-1]
           +  alpha*gamma*self.f_values[x_pos,y_pos,z_pos]) -
           (  (1-alpha)*(1-gamma)*self.f_values[x_pos-1,y_pos-1,z_pos-1]
           +  (1-alpha)*gamma*self.f_values[x_pos-1,y_pos-1,z_pos]
           +  alpha*(1-gamma)*self.f_values[x_pos,y_pos-1,z_pos-1]
           +  alpha*gamma*self.f_values[x_pos,y_pos-1,z_pos]))/(self.y_list[y_pos] - self.y_list[y_pos-1])
        return dfdy
        
    def _derZ(self,x,y,z):
        '''
        Returns the derivative with respect to z of the interpolated function
        at each value in x,y,z. Only called internally by HARKinterpolator3D.derivativeZ.
        '''
        if _isscalar(x):
            x_pos = max(min(self.xSearchFunc(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(self.ySearchFunc(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(self.zSearchFunc(self.z_list,z),self.z_n-1),1)
        else:
            x_pos = self.xSearchFunc(self.x_list,x)
            x_pos[x_pos < 1] = 1
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = self.ySearchFunc(self.y_list,y)
            y_pos[y_pos < 1] = 1
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            z_pos = self.zSearchFunc(self.z_list,z)
            z_pos[z_pos < 1] = 1
            z_pos[z_pos > self.z_n-1] = self.z_n-1
        alpha = (x - self.x_list[x_pos-1])/(self.x_list[x_pos] - self.x_list[x_pos-1])
        beta = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
        dfdz = (
           (  (1-alpha)*(1-beta)*self.f_values[x_pos-1,y_pos-1,z_pos]
           +  (1-alpha)*beta*self.f_values[x_pos-1,y_pos,z_pos]
           +  alpha*(1-beta)*self.f_values[x_pos,y_pos-1,z_pos]
           +  alpha*beta*self.f_values[x_pos,y_pos,z_pos]) -
           (  (1-alpha)*(1-beta)*self.f_values[x_pos-1,y_pos-1,z_pos-1]
           +  (1-alpha)*beta*self.f_values[x_pos-1,y_pos,z_pos-1]
           +  alpha*(1-beta)*self.f_values[x_pos,y_pos-1,z_pos-1]
           +  alpha*beta*self.f_values[x_pos,y_pos,z_pos-1]))/(self.z_list[z_pos] - self.z_list[z_pos-1])
        return dfdz
        

class QuadlinearInterp(HARKinterpolator4D):
    '''
    Quadlinear full (or tensor) grid interpolation of a function f(w,x,y,z).
    '''
    distance_criteria = ['f_values','w_list','x_list','y_list','z_list']
    
    def __init__(self,f_values,w_list,x_list,y_list,z_list,wSearchFunc=None,xSearchFunc=None,ySearchFunc=None,zSearchFunc=None):
        '''
        Constructor to make a new quadlinear interpolation.
        
        Parameters
        ----------
        f_values : numpy.array
            An array of size (w_n,x_n,y_n,z_n) such that f_values[i,j,k,l] =
            f(w_list[i],x_list[j],y_list[k],z_list[l])
        w_list : numpy.array
            An array of x values, with length designated w_n.
        x_list : numpy.array
            An array of x values, with length designated x_n.
        y_list : numpy.array
            An array of y values, with length designated y_n.
        z_list : numpy.array
            An array of z values, with length designated z_n.
        wSearchFunc : function
            An optional function that returns the reference location for w values:
            indices = wSearchFunc(w_list,w).  Default is np.searchsorted
        xSearchFunc : function
            An optional function that returns the reference location for x values:
            indices = xSearchFunc(x_list,x).  Default is np.searchsorted
        ySearchFunc : function
            An optional function that returns the reference location for y values:
            indices = ySearchFunc(y_list,y).  Default is np.searchsorted
        zSearchFunc : function
            An optional function that returns the reference location for z values:
            indices = zSearchFunc(z_list,z).  Default is np.searchsorted
            
        Returns
        -------
        new instance of QuadlinearInterp
        '''
        self.f_values = f_values
        self.w_list = w_list
        self.x_list = x_list
        self.y_list = y_list
        self.z_list = z_list
        self.w_n = w_list.size
        self.x_n = x_list.size
        self.y_n = y_list.size
        self.z_n = z_list.size
        if wSearchFunc is None:
            wSearchFunc = np.searchsorted
        if xSearchFunc is None:
            xSearchFunc = np.searchsorted
        if ySearchFunc is None:
            ySearchFunc = np.searchsorted
        if zSearchFunc is None:
            zSearchFunc = np.searchsorted
        self.wSearchFunc = wSearchFunc
        self.xSearchFunc = xSearchFunc
        self.ySearchFunc = ySearchFunc
        self.zSearchFunc = zSearchFunc
        
    def _evaluate(self,w,x,y,z):
        '''
        Returns the level of the interpolated function at each value in x,y,z.
        Only called internally by HARKinterpolator4D.__call__ (etc).
        '''
        if _isscalar(w):
            w_pos = max(min(self.wSearchFunc(self.w_list,w),self.w_n-1),1)
            x_pos = max(min(self.xSearchFunc(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(self.ySearchFunc(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(self.zSearchFunc(self.z_list,z),self.z_n-1),1)
        else:
            w_pos = self.wSearchFunc(self.w_list,w)
            w_pos[w_pos < 1] = 1
            w_pos[w_pos > self.w_n-1] = self.w_n-1
            x_pos = self.xSearchFunc(self.x_list,x)
            x_pos[x_pos < 1] = 1
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = self.ySearchFunc(self.y_list,y)
            y_pos[y_pos < 1] = 1
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            z_pos = self.zSearchFunc(self.z_list,z)
            z_pos[z_pos < 1] = 1
            z_pos[z_pos > self.z_n-1] = self.z_n-1
        i = w_pos # for convenience
        j = x_pos
        k = y_pos
        l = z_pos
        alpha = (w - self.w_list[i-1])/(self.w_list[i] - self.w_list[i-1])
        beta = (x - self.x_list[j-1])/(self.x_list[j] - self.x_list[j-1])
        gamma = (y - self.y_list[k-1])/(self.y_list[k] - self.y_list[k-1])
        delta = (z - self.z_list[l-1])/(self.z_list[l] - self.z_list[l-1])
        f = (
             (1-alpha)*((1-beta)*((1-gamma)*(1-delta)*self.f_values[i-1,j-1,k-1,l-1]
           + (1-gamma)*delta*self.f_values[i-1,j-1,k-1,l]
           + gamma*(1-delta)*self.f_values[i-1,j-1,k,l-1]
           + gamma*delta*self.f_values[i-1,j-1,k,l])
           + beta*((1-gamma)*(1-delta)*self.f_values[i-1,j,k-1,l-1]
           + (1-gamma)*delta*self.f_values[i-1,j,k-1,l]
           + gamma*(1-delta)*self.f_values[i-1,j,k,l-1]
           + gamma*delta*self.f_values[i-1,j,k,l]))
           + alpha*((1-beta)*((1-gamma)*(1-delta)*self.f_values[i,j-1,k-1,l-1]
           + (1-gamma)*delta*self.f_values[i,j-1,k-1,l]
           + gamma*(1-delta)*self.f_values[i,j-1,k,l-1]
           + gamma*delta*self.f_values[i,j-1,k,l])
           + beta*((1-gamma)*(1-delta)*self.f_values[i,j,k-1,l-1]
           + (1-gamma)*delta*self.f_values[i,j,k-1,l]
           + gamma*(1-delta)*self.f_values[i,j,k,l-1]
           + gamma*delta*self.f_values[i,j,k,l])))       
        return f
        
    def _derW(self,w,x,y,z):
        '''
        Returns the derivative with respect to w of the interpolated function
        at each value in w,x,y,z. Only called internally by HARKinterpolator4D.derivativeW.
        '''
        if _isscalar(w):
            w_pos = max(min(self.wSearchFunc(self.w_list,w),self.w_n-1),1)
            x_pos = max(min(self.xSearchFunc(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(self.ySearchFunc(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(self.zSearchFunc(self.z_list,z),self.z_n-1),1)
        else:
            w_pos = self.wSearchFunc(self.w_list,w)
            w_pos[w_pos < 1] = 1
            w_pos[w_pos > self.w_n-1] = self.w_n-1
            x_pos = self.xSearchFunc(self.x_list,x)
            x_pos[x_pos < 1] = 1
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = self.ySearchFunc(self.y_list,y)
            y_pos[y_pos < 1] = 1
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            z_pos = self.zSearchFunc(self.z_list,z)
            z_pos[z_pos < 1] = 1
            z_pos[z_pos > self.z_n-1] = self.z_n-1
        i = w_pos # for convenience
        j = x_pos
        k = y_pos
        l = z_pos
        beta = (x - self.x_list[j-1])/(self.x_list[j] - self.x_list[j-1])
        gamma = (y - self.y_list[k-1])/(self.y_list[k] - self.y_list[k-1])
        delta = (z - self.z_list[l-1])/(self.z_list[l] - self.z_list[l-1])
        dfdw = (
          (  (1-beta)*(1-gamma)*(1-delta)*self.f_values[i,j-1,k-1,l-1]
           + (1-beta)*(1-gamma)*delta*self.f_values[i,j-1,k-1,l]
           + (1-beta)*gamma*(1-delta)*self.f_values[i,j-1,k,l-1]
           + (1-beta)*gamma*delta*self.f_values[i,j-1,k,l]
           + beta*(1-gamma)*(1-delta)*self.f_values[i,j,k-1,l-1]
           + beta*(1-gamma)*delta*self.f_values[i,j,k-1,l]
           + beta*gamma*(1-delta)*self.f_values[i,j,k,l-1]
           + beta*gamma*delta*self.f_values[i,j,k,l] ) - 
          (  (1-beta)*(1-gamma)*(1-delta)*self.f_values[i-1,j-1,k-1,l-1]
           + (1-beta)*(1-gamma)*delta*self.f_values[i-1,j-1,k-1,l]
           + (1-beta)*gamma*(1-delta)*self.f_values[i-1,j-1,k,l-1]
           + (1-beta)*gamma*delta*self.f_values[i-1,j-1,k,l]
           + beta*(1-gamma)*(1-delta)*self.f_values[i-1,j,k-1,l-1]
           + beta*(1-gamma)*delta*self.f_values[i-1,j,k-1,l]
           + beta*gamma*(1-delta)*self.f_values[i-1,j,k,l-1]
           + beta*gamma*delta*self.f_values[i-1,j,k,l] )
              )/(self.w_list[i] - self.w_list[i-1])
        return dfdw
        
    def _derX(self,w,x,y,z):
        '''
        Returns the derivative with respect to x of the interpolated function
        at each value in w,x,y,z. Only called internally by HARKinterpolator4D.derivativeX.
        '''
        if _isscalar(w):
            w_pos = max(min(self.wSearchFunc(self.w_list,w),self.w_n-1),1)
            x_pos = max(min(self.xSearchFunc(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(self.ySearchFunc(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(self.zSearchFunc(self.z_list,z),self.z_n-1),1)
        else:
            w_pos = self.wSearchFunc(self.w_list,w)
            w_pos[w_pos < 1] = 1
            w_pos[w_pos > self.w_n-1] = self.w_n-1
            x_pos = self.xSearchFunc(self.x_list,x)
            x_pos[x_pos < 1] = 1
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = self.ySearchFunc(self.y_list,y)
            y_pos[y_pos < 1] = 1
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            z_pos = self.zSearchFunc(self.z_list,z)
            z_pos[z_pos < 1] = 1
            z_pos[z_pos > self.z_n-1] = self.z_n-1
        i = w_pos # for convenience
        j = x_pos
        k = y_pos
        l = z_pos
        alpha = (w - self.w_list[i-1])/(self.w_list[i] - self.w_list[i-1])
        gamma = (y - self.y_list[k-1])/(self.y_list[k] - self.y_list[k-1])
        delta = (z - self.z_list[l-1])/(self.z_list[l] - self.z_list[l-1])
        dfdx = (
          (  (1-alpha)*(1-gamma)*(1-delta)*self.f_values[i-1,j,k-1,l-1]
           + (1-alpha)*(1-gamma)*delta*self.f_values[i-1,j,k-1,l]
           + (1-alpha)*gamma*(1-delta)*self.f_values[i-1,j,k,l-1]
           + (1-alpha)*gamma*delta*self.f_values[i-1,j,k,l]
           + alpha*(1-gamma)*(1-delta)*self.f_values[i,j,k-1,l-1]
           + alpha*(1-gamma)*delta*self.f_values[i,j,k-1,l]
           + alpha*gamma*(1-delta)*self.f_values[i,j,k,l-1]
           + alpha*gamma*delta*self.f_values[i,j,k,l] ) - 
          (  (1-alpha)*(1-gamma)*(1-delta)*self.f_values[i-1,j-1,k-1,l-1]
           + (1-alpha)*(1-gamma)*delta*self.f_values[i-1,j-1,k-1,l]
           + (1-alpha)*gamma*(1-delta)*self.f_values[i-1,j-1,k,l-1]
           + (1-alpha)*gamma*delta*self.f_values[i-1,j-1,k,l]
           + alpha*(1-gamma)*(1-delta)*self.f_values[i,j-1,k-1,l-1]
           + alpha*(1-gamma)*delta*self.f_values[i,j-1,k-1,l]
           + alpha*gamma*(1-delta)*self.f_values[i,j-1,k,l-1]
           + alpha*gamma*delta*self.f_values[i,j-1,k,l] )
              )/(self.x_list[j] - self.x_list[j-1])
        return dfdx
        
    def _derY(self,w,x,y,z):
        '''
        Returns the derivative with respect to y of the interpolated function
        at each value in w,x,y,z. Only called internally by HARKinterpolator4D.derivativeY.
        '''
        if _isscalar(w):
            w_pos = max(min(self.wSearchFunc(self.w_list,w),self.w_n-1),1)
            x_pos = max(min(self.xSearchFunc(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(self.ySearchFunc(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(self.zSearchFunc(self.z_list,z),self.z_n-1),1)
        else:
            w_pos = self.wSearchFunc(self.w_list,w)
            w_pos[w_pos < 1] = 1
            w_pos[w_pos > self.w_n-1] = self.w_n-1
            x_pos = self.xSearchFunc(self.x_list,x)
            x_pos[x_pos < 1] = 1
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = self.ySearchFunc(self.y_list,y)
            y_pos[y_pos < 1] = 1
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            z_pos = self.zSearchFunc(self.z_list,z)
            z_pos[z_pos < 1] = 1
            z_pos[z_pos > self.z_n-1] = self.z_n-1
        i = w_pos # for convenience
        j = x_pos
        k = y_pos
        l = z_pos
        alpha = (w - self.w_list[i-1])/(self.w_list[i] - self.w_list[i-1])
        beta = (x - self.x_list[j-1])/(self.x_list[j] - self.x_list[j-1])
        delta = (z - self.z_list[l-1])/(self.z_list[l] - self.z_list[l-1])
        dfdy = (
          (  (1-alpha)*(1-beta)*(1-delta)*self.f_values[i-1,j-1,k,l-1]
           + (1-alpha)*(1-beta)*delta*self.f_values[i-1,j-1,k,l]
           + (1-alpha)*beta*(1-delta)*self.f_values[i-1,j,k,l-1]
           + (1-alpha)*beta*delta*self.f_values[i-1,j,k,l]
           + alpha*(1-beta)*(1-delta)*self.f_values[i,j-1,k,l-1]
           + alpha*(1-beta)*delta*self.f_values[i,j-1,k,l]
           + alpha*beta*(1-delta)*self.f_values[i,j,k,l-1]
           + alpha*beta*delta*self.f_values[i,j,k,l] ) - 
          (  (1-alpha)*(1-beta)*(1-delta)*self.f_values[i-1,j-1,k-1,l-1]
           + (1-alpha)*(1-beta)*delta*self.f_values[i-1,j-1,k-1,l]
           + (1-alpha)*beta*(1-delta)*self.f_values[i-1,j,k-1,l-1]
           + (1-alpha)*beta*delta*self.f_values[i-1,j,k-1,l]
           + alpha*(1-beta)*(1-delta)*self.f_values[i,j-1,k-1,l-1]
           + alpha*(1-beta)*delta*self.f_values[i,j-1,k-1,l]
           + alpha*beta*(1-delta)*self.f_values[i,j,k-1,l-1]
           + alpha*beta*delta*self.f_values[i,j,k-1,l] )
              )/(self.y_list[k] - self.y_list[k-1])
        return dfdy
        
    def _derZ(self,w,x,y,z):
        '''
        Returns the derivative with respect to z of the interpolated function
        at each value in w,x,y,z. Only called internally by HARKinterpolator4D.derivativeZ.
        '''
        if _isscalar(w):
            w_pos = max(min(self.wSearchFunc(self.w_list,w),self.w_n-1),1)
            x_pos = max(min(self.xSearchFunc(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(self.ySearchFunc(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(self.zSearchFunc(self.z_list,z),self.z_n-1),1)
        else:
            w_pos = self.wSearchFunc(self.w_list,w)
            w_pos[w_pos < 1] = 1
            w_pos[w_pos > self.w_n-1] = self.w_n-1
            x_pos = self.xSearchFunc(self.x_list,x)
            x_pos[x_pos < 1] = 1
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = self.ySearchFunc(self.y_list,y)
            y_pos[y_pos < 1] = 1
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            z_pos = self.zSearchFunc(self.z_list,z)
            z_pos[z_pos < 1] = 1
            z_pos[z_pos > self.z_n-1] = self.z_n-1
        i = w_pos # for convenience
        j = x_pos
        k = y_pos
        l = z_pos
        alpha = (w - self.w_list[i-1])/(self.w_list[i] - self.w_list[i-1])
        beta = (x - self.x_list[j-1])/(self.x_list[j] - self.x_list[j-1])
        gamma = (y - self.y_list[k-1])/(self.y_list[k] - self.y_list[k-1])
        dfdz = (
          (  (1-alpha)*(1-beta)*(1-gamma)*self.f_values[i-1,j-1,k-1,l]
           + (1-alpha)*(1-beta)*gamma*self.f_values[i-1,j-1,k,l]
           + (1-alpha)*beta*(1-gamma)*self.f_values[i-1,j,k-1,l]
           + (1-alpha)*beta*gamma*self.f_values[i-1,j,k,l]
           + alpha*(1-beta)*(1-gamma)*self.f_values[i,j-1,k-1,l]
           + alpha*(1-beta)*gamma*self.f_values[i,j-1,k,l]
           + alpha*beta*(1-gamma)*self.f_values[i,j,k-1,l]
           + alpha*beta*gamma*self.f_values[i,j,k,l] ) - 
          (  (1-alpha)*(1-beta)*(1-gamma)*self.f_values[i-1,j-1,k-1,l-1]
           + (1-alpha)*(1-beta)*gamma*self.f_values[i-1,j-1,k,l-1]
           + (1-alpha)*beta*(1-gamma)*self.f_values[i-1,j,k-1,l-1]
           + (1-alpha)*beta*gamma*self.f_values[i-1,j,k,l-1]
           + alpha*(1-beta)*(1-gamma)*self.f_values[i,j-1,k-1,l-1]
           + alpha*(1-beta)*gamma*self.f_values[i,j-1,k,l-1]
           + alpha*beta*(1-gamma)*self.f_values[i,j,k-1,l-1]
           + alpha*beta*gamma*self.f_values[i,j,k,l-1] )
              )/(self.z_list[l] - self.z_list[l-1])
        return dfdz
        

class LowerEnvelope(HARKinterpolator1D):
    '''
    The lower envelope of a finite set of 1D functions, each of which can be of
    any class that has the methods __call__, derivative, and eval_with_derivative.
    Generally: it combines HARKinterpolator1Ds. 
    '''
    distance_criteria = ['functions']

    def __init__(self,*functions):
        '''
        Constructor to make a new lower envelope iterpolation.
        
        Parameters
        ----------
        *functions : function
            Any number of real functions; often instances of HARKinterpolator1D
            
        Returns
        -------
        new instance of LowerEnvelope
        '''
        self.functions = []
        for function in functions:
            self.functions.append(function)
        self.funcCount = len(self.functions)

    def _evaluate(self,x):
        '''
        Returns the level of the function at each value in x as the minimum among
        all of the functions.  Only called internally by HARKinterpolator1D.__call__.
        '''
        if _isscalar(x):
            y = np.nanmin([f(x) for f in self.functions])
        else:
            m = len(x)
            fx = np.zeros((m,self.funcCount))
            for j in range(self.funcCount):
                fx[:,j] = self.functions[j](x)
            y = np.nanmin(fx,axis=1)       
        return y

    def _der(self,x):
        '''
        Returns the first derivative of the function at each value in x.  Only
        called internally by HARKinterpolator1D.derivative.
        '''
        y,dydx = self.eval_with_derivative(x)
        return dydx  # Sadly, this is the fastest / most convenient way...

    def _evalAndDer(self,x):
        '''
        Returns the level and first derivative of the function at each value in
        x.  Only called internally by HARKinterpolator1D.eval_and_der.
        '''
        m = len(x)
        fx = np.zeros((m,self.funcCount))
        for j in range(self.funcCount):
            fx[:,j] = self.functions[j](x)
        fx[np.isnan(fx)] = np.inf
        i = np.argmin(fx,axis=1)
        y = fx[np.arange(m),i]
        dydx = np.zeros_like(y)
        for j in range(self.funcCount):
            c = i == j
            dydx[c] = self.functions[j].derivative(x[c])
        return y,dydx


class UpperEnvelope(HARKinterpolator1D):
    '''
    The upper envelope of a finite set of 1D functions, each of which can be of
    any class that has the methods __call__, derivative, and eval_with_derivative.
    Generally: it combines HARKinterpolator1Ds. 
    '''
    distance_criteria = ['functions']

    def __init__(self,*functions):
        '''
        Constructor to make a new upper envelope iterpolation.
        
        Parameters
        ----------
        *functions : function
            Any number of real functions; often instances of HARKinterpolator1D
            
        Returns
        -------
        new instance of UpperEnvelope
        '''
        self.functions = []
        for function in functions:
            self.functions.append(function)
        self.funcCount = len(self.functions)

    def _evaluate(self,x):
        '''
        Returns the level of the function at each value in x as the maximum among
        all of the functions.  Only called internally by HARKinterpolator1D.__call__.
        '''
        if _isscalar(x):
            y = np.nanmax([f(x) for f in self.functions])
        else:
            m = len(x)
            fx = np.zeros((m,self.funcCount))
            for j in range(self.funcCount):
                fx[:,j] = self.functions[j](x)
            y = np.nanmax(fx,axis=1)       
        return y

    def _der(self,x):
        '''
        Returns the first derivative of the function at each value in x.  Only
        called internally by HARKinterpolator1D.derivative.
        '''
        y,dydx = self.eval_with_derivative(x)
        return dydx  # Sadly, this is the fastest / most convenient way...

    def _evalAndDer(self,x):
        '''
        Returns the level and first derivative of the function at each value in
        x.  Only called internally by HARKinterpolator1D.eval_and_der.
        '''
        m = len(x)
        fx = np.zeros((m,self.funcCount))
        for j in range(self.funcCount):
            fx[:,j] = self.functions[j](x)
        fx[np.isnan(fx)] = np.inf
        i = np.argmax(fx,axis=1)
        y = fx[np.arange(m),i]
        dydx = np.zeros_like(y)
        for j in range(self.funcCount):
            c = i == j
            dydx[c] = self.functions[j].derivative(x[c])
        return y,dydx
        
        
class LowerEnvelope2D(HARKinterpolator2D):
    '''
    The lower envelope of a finite set of 2D functions, each of which can be of
    any class that has the methods __call__, derivativeX, and derivativeY.
    Generally: it combines HARKinterpolator2Ds. 
    '''
    distance_criteria = ['functions']

    def __init__(self,*functions):
        '''
        Constructor to make a new lower envelope iterpolation.
        
        Parameters
        ----------
        *functions : function
            Any number of real functions; often instances of HARKinterpolator2D
            
        Returns
        -------
        new instance of LowerEnvelope2D
        '''
        self.functions = []
        for function in functions:
            self.functions.append(function)
        self.funcCount = len(self.functions)

    def _evaluate(self,x,y):
        '''
        Returns the level of the function at each value in (x,y) as the minimum
        among all of the functions.  Only called internally by
        HARKinterpolator2D.__call__.
        '''
        if _isscalar(x):
            f = np.nanmin([f(x,y) for f in self.functions])
        else:
            m = len(x)
            temp = np.zeros((m,self.funcCount))
            for j in range(self.funcCount):
                temp[:,j] = self.functions[j](x,y)
            f = np.nanmin(temp,axis=1)       
        return f

    def _derX(self,x,y):
        '''
        Returns the first derivative of the function with respect to X at each
        value in (x,y).  Only called internally by HARKinterpolator2D._derX.
        '''
        m = len(x)
        temp = np.zeros((m,self.funcCount))
        for j in range(self.funcCount):
            temp[:,j] = self.functions[j](x,y)
        temp[np.isnan(temp)] = np.inf
        i = np.argmin(temp,axis=1)
        dfdx = np.zeros_like(x)
        for j in range(self.funcCount):
            c = i == j
            dfdx[c] = self.functions[j].derivativeX(x[c],y[c])
        return dfdx
        
    def _derY(self,x,y):
        '''
        Returns the first derivative of the function with respect to Y at each
        value in (x,y).  Only called internally by HARKinterpolator2D._derY.
        '''
        m = len(x)
        temp = np.zeros((m,self.funcCount))
        for j in range(self.funcCount):
            temp[:,j] = self.functions[j](x,y)
        temp[np.isnan(temp)] = np.inf
        i = np.argmin(temp,axis=1)
        y = temp[np.arange(m),i]
        dfdy = np.zeros_like(x)
        for j in range(self.funcCount):
            c = i == j
            dfdy[c] = self.functions[j].derivativeY(x[c],y[c])
        return dfdy
        
    
class LowerEnvelope3D(HARKinterpolator3D):
    '''
    The lower envelope of a finite set of 3D functions, each of which can be of
    any class that has the methods __call__, derivativeX, derivativeY, and
    derivativeZ. Generally: it combines HARKinterpolator2Ds. 
    '''
    distance_criteria = ['functions']

    def __init__(self,*functions):
        '''
        Constructor to make a new lower envelope iterpolation.
        
        Parameters
        ----------
        *functions : function
            Any number of real functions; often instances of HARKinterpolator3D
            
        Returns
        -------
        None
        '''
        self.functions = []
        for function in functions:
            self.functions.append(function)
        self.funcCount = len(self.functions)

    def _evaluate(self,x,y,z):
        '''
        Returns the level of the function at each value in (x,y,z) as the minimum
        among all of the functions.  Only called internally by
        HARKinterpolator3D.__call__.
        '''
        if _isscalar(x):
            f = np.nanmin([f(x,y,z) for f in self.functions])
        else:
            m = len(x)
            temp = np.zeros((m,self.funcCount))
            for j in range(self.funcCount):
                temp[:,j] = self.functions[j](x,y,z)
            f = np.nanmin(temp,axis=1)       
        return f

    def _derX(self,x,y,z):
        '''
        Returns the first derivative of the function with respect to X at each
        value in (x,y,z).  Only called internally by HARKinterpolator3D._derX.
        '''
        m = len(x)
        temp = np.zeros((m,self.funcCount))
        for j in range(self.funcCount):
            temp[:,j] = self.functions[j](x,y,z)
        temp[np.isnan(temp)] = np.inf
        i = np.argmin(temp,axis=1)
        dfdx = np.zeros_like(x)
        for j in range(self.funcCount):
            c = i == j
            dfdx[c] = self.functions[j].derivativeX(x[c],y[c],z[c])
        return dfdx
        
    def _derY(self,x,y,z):
        '''
        Returns the first derivative of the function with respect to Y at each
        value in (x,y,z).  Only called internally by HARKinterpolator3D._derY.
        '''
        m = len(x)
        temp = np.zeros((m,self.funcCount))
        for j in range(self.funcCount):
            temp[:,j] = self.functions[j](x,y,z)
        temp[np.isnan(temp)] = np.inf
        i = np.argmin(temp,axis=1)
        y = temp[np.arange(m),i]
        dfdy = np.zeros_like(x)
        for j in range(self.funcCount):
            c = i == j
            dfdy[c] = self.functions[j].derivativeY(x[c],y[c],z[c])
        return dfdy

    def _derZ(self,x,y,z):
        '''
        Returns the first derivative of the function with respect to Z at each
        value in (x,y,z).  Only called internally by HARKinterpolator3D._derZ.
        '''
        m = len(x)
        temp = np.zeros((m,self.funcCount))
        for j in range(self.funcCount):
            temp[:,j] = self.functions[j](x,y,z)
        temp[np.isnan(temp)] = np.inf
        i = np.argmin(temp,axis=1)
        y = temp[np.arange(m),i]
        dfdz = np.zeros_like(x)
        for j in range(self.funcCount):
            c = i == j
            dfdz[c] = self.functions[j].derivativeZ(x[c],y[c],z[c])
        return dfdz
        
        
class VariableLowerBoundFunc2D(HARKobject):
    '''
    A class for representing a function with two real inputs whose lower bound
    in the first input depends on the second input.  Useful for managing curved
    natural borrowing constraints, as occurs in the persistent shocks model.
    '''
    distance_criteria = ['func','lowerBound']
    
    def __init__(self,func,lowerBound):
        '''
        Make a new instance of VariableLowerBoundFunc2D.
        
        Parameters
        ----------
        func : function
            A function f: (R_+ x R) --> R representing the function of interest
            shifted by its lower bound in the first input.
        lowerBound : function
            The lower bound in the first input of the function of interest, as
            a function of the second input.
            
        Returns
        -------
        None
        '''
        self.func = func
        self.lowerBound = lowerBound
        
    def __call__(self,x,y):
        '''
        Evaluate the function at given state space points.
        
        Parameters
        ----------
        x : np.array
             First input values.
        y : np.array
             Second input values; should be of same shape as x.
             
        Returns
        -------
        f_out : np.array
            Function evaluated at (x,y), of same shape as inputs.
        '''
        xShift = self.lowerBound(y)
        f_out = self.func(x-xShift,y)
        return f_out
        
    def derivativeX(self,x,y):
        '''
        Evaluate the first derivative with respect to x of the function at given
        state space points.
        
        Parameters
        ----------
        x : np.array
             First input values.
        y : np.array
             Second input values; should be of same shape as x.
             
        Returns
        -------
        dfdx_out : np.array
            First derivative of function with respect to the first input, 
            evaluated at (x,y), of same shape as inputs.
        '''
        xShift = self.lowerBound(y)
        dfdx_out = self.func.derivativeX(x-xShift,y)
        return dfdx_out
        
    def derivativeY(self,x,y):
        '''
        Evaluate the first derivative with respect to y of the function at given
        state space points.
        
        Parameters
        ----------
        x : np.array
             First input values.
        y : np.array
             Second input values; should be of same shape as x.
             
        Returns
        -------
        dfdy_out : np.array
            First derivative of function with respect to the second input, 
            evaluated at (x,y), of same shape as inputs.
        '''
        xShift,xShiftDer = self.lowerBound.eval_with_derivative(y)
        dfdy_out = self.func.derivativeY(x-xShift,y) - xShiftDer*self.func.derivativeX(x-xShift,y)
        return dfdy_out
        
        
class VariableLowerBoundFunc3D(HARKobject):
    '''
    A class for representing a function with three real inputs whose lower bound
    in the first input depends on the second input.  Useful for managing curved
    natural borrowing constraints.
    '''
    distance_criteria = ['func','lowerBound']
    
    def __init__(self,func,lowerBound):
        '''
        Make a new instance of VariableLowerBoundFunc3D.
        
        Parameters
        ----------
        func : function
            A function f: (R_+ x R^2) --> R representing the function of interest
            shifted by its lower bound in the first input.
        lowerBound : function
            The lower bound in the first input of the function of interest, as
            a function of the second input.
            
        Returns
        -------
        None
        '''
        self.func = func
        self.lowerBound = lowerBound
        
    def __call__(self,x,y,z):
        '''
        Evaluate the function at given state space points.
        
        Parameters
        ----------
        x : np.array
             First input values.
        y : np.array
             Second input values; should be of same shape as x.
        z : np.array
             Third input values; should be of same shape as x.
             
        Returns
        -------
        f_out : np.array
            Function evaluated at (x,y,z), of same shape as inputs.
        '''
        xShift = self.lowerBound(y)
        f_out = self.func(x-xShift,y,z)
        return f_out
        
    def derivativeX(self,x,y,z):
        '''
        Evaluate the first derivative with respect to x of the function at given
        state space points.
        
        Parameters
        ----------
        x : np.array
             First input values.
        y : np.array
             Second input values; should be of same shape as x.
        z : np.array
             Third input values; should be of same shape as x.
             
        Returns
        -------
        dfdx_out : np.array
            First derivative of function with respect to the first input, 
            evaluated at (x,y,z), of same shape as inputs.
        '''
        xShift = self.lowerBound(y)
        dfdx_out = self.func.derivativeX(x-xShift,y,z)
        return dfdx_out
        
    def derivativeY(self,x,y,z):
        '''
        Evaluate the first derivative with respect to y of the function at given
        state space points.
        
        Parameters
        ----------
        x : np.array
             First input values.
        y : np.array
             Second input values; should be of same shape as x.
        z : np.array
             Third input values; should be of same shape as x.
             
        Returns
        -------
        dfdy_out : np.array
            First derivative of function with respect to the second input, 
            evaluated at (x,y,z), of same shape as inputs.
        '''
        xShift,xShiftDer = self.lowerBound.eval_with_derivative(y)
        dfdy_out = self.func.derivativeY(x-xShift,y,z) - \
                   xShiftDer*self.func.derivativeX(x-xShift,y,z)
        return dfdy_out
        
    def derivativeZ(self,x,y,z):
        '''
        Evaluate the first derivative with respect to z of the function at given
        state space points.
        
        Parameters
        ----------
        x : np.array
             First input values.
        y : np.array
             Second input values; should be of same shape as x.
        z : np.array
             Third input values; should be of same shape as x.
             
        Returns
        -------
        dfdz_out : np.array
            First derivative of function with respect to the third input, 
            evaluated at (x,y,z), of same shape as inputs.
        '''
        xShift = self.lowerBound(y)
        dfdz_out = self.func.derivativeZ(x-xShift,y,z)
        return dfdz_out


class LinearInterpOnInterp1D(HARKinterpolator2D):
    '''
    A 2D interpolator that linearly interpolates among a list of 1D interpolators.
    '''
    distance_criteria = ['xInterpolators','y_list']
    def __init__(self,xInterpolators,y_values):
        '''
        Constructor for the class, generating an approximation to a function of
        the form f(x,y) using interpolations over f(x,y_0) for a fixed grid of
        y_0 values.
        
        Parameters
        ----------
        xInterpolators : [HARKinterpolator1D]
            A list of 1D interpolations over the x variable.  The nth element of
            xInterpolators represents f(x,y_values[n]).
        y_values: numpy.array
            An array of y values equal in length to xInterpolators.
            
        Returns
        -------
        new instance of LinearInterpOnInterp1D
        '''
        self.xInterpolators = xInterpolators
        self.y_list = y_values
        self.y_n = y_values.size
        
    def _evaluate(self,x,y):
        '''
        Returns the level of the interpolated function at each value in x,y.
        Only called internally by HARKinterpolator2D.__call__ (etc).
        '''
        if _isscalar(x):
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            alpha = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
            f = (1-alpha)*self.xInterpolators[y_pos-1](x) + alpha*self.xInterpolators[y_pos](x)
        else:
            m = len(x)
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            f = np.zeros(m) + np.nan
            if y.size > 0:
                for i in xrange(1,self.y_n):
                    c = y_pos == i
                    if np.any(c):
                        alpha = (y[c] - self.y_list[i-1])/(self.y_list[i] - self.y_list[i-1])
                        f[c] = (1-alpha)*self.xInterpolators[i-1](x[c]) + alpha*self.xInterpolators[i](x[c]) 
        return f
        
    def _derX(self,x,y):
        '''
        Returns the derivative with respect to x of the interpolated function
        at each value in x,y. Only called internally by HARKinterpolator2D.derivativeX.
        '''
        if _isscalar(x):
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            alpha = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
            dfdx = (1-alpha)*self.xInterpolators[y_pos-1]._der(x) + alpha*self.xInterpolators[y_pos]._der(x)
        else:
            m = len(x)
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            dfdx = np.zeros(m) + np.nan
            if y.size > 0:
                for i in xrange(1,self.y_n):
                    c = y_pos == i
                    if np.any(c):
                        alpha = (y[c] - self.y_list[i-1])/(self.y_list[i] - self.y_list[i-1])
                        dfdx[c] = (1-alpha)*self.xInterpolators[i-1]._der(x[c]) + alpha*self.xInterpolators[i]._der(x[c])
        return dfdx
        
    def _derY(self,x,y):
        '''
        Returns the derivative with respect to y of the interpolated function
        at each value in x,y. Only called internally by HARKinterpolator2D.derivativeY.
        '''
        if _isscalar(x):
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            dfdy = (self.xInterpolators[y_pos](x) - self.xInterpolators[y_pos-1](x))/(self.y_list[y_pos] - self.y_list[y_pos-1])
        else:
            m = len(x)
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            dfdy = np.zeros(m) + np.nan
            if y.size > 0:
                for i in xrange(1,self.y_n):
                    c = y_pos == i
                    if np.any(c):
                        dfdy[c] = (self.xInterpolators[i](x[c]) - self.xInterpolators[i-1](x[c]))/(self.y_list[i] - self.y_list[i-1])
        return dfdy


class BilinearInterpOnInterp1D(HARKinterpolator3D):
    '''
    A 3D interpolator that bilinearly interpolates among a list of lists of 1D
    interpolators.
    '''
    distance_criteria = ['xInterpolators','y_list','z_list']
    
    def __init__(self,xInterpolators,y_values,z_values):
        '''
        Constructor for the class, generating an approximation to a function of
        the form f(x,y,z) using interpolations over f(x,y_0,z_0) for a fixed grid
        of y_0 and z_0 values.
        
        Parameters
        ----------
        xInterpolators : [[HARKinterpolator1D]]
            A list of lists of 1D interpolations over the x variable.  The i,j-th
            element of xInterpolators represents f(x,y_values[i],z_values[j]).
        y_values: numpy.array
            An array of y values equal in length to xInterpolators.
        z_values: numpy.array
            An array of z values equal in length to xInterpolators[0].
            
        Returns
        -------
        new instance of BilinearInterpOnInterp1D
        '''
        self.xInterpolators = xInterpolators
        self.y_list = y_values
        self.y_n = y_values.size
        self.z_list = z_values
        self.z_n = z_values.size
        
    def _evaluate(self,x,y,z):
        '''
        Returns the level of the interpolated function at each value in x,y,z.
        Only called internally by HARKinterpolator3D.__call__ (etc).
        '''
        if _isscalar(x):
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
            beta = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            f = ((1-alpha)*(1-beta)*self.xInterpolators[y_pos-1][z_pos-1](x)
              + (1-alpha)*beta*self.xInterpolators[y_pos-1][z_pos](x)
              + alpha*(1-beta)*self.xInterpolators[y_pos][z_pos-1](x)
              + alpha*beta*self.xInterpolators[y_pos][z_pos](x))              
        else:
            m = len(x)
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            f = np.zeros(m) + np.nan
            for i in xrange(1,self.y_n):
                for j in xrange(1,self.z_n):
                    c = np.logical_and(i == y_pos, j == z_pos)
                    if np.any(c):
                        alpha = (y[c] - self.y_list[i-1])/(self.y_list[i] - self.y_list[i-1])
                        beta = (z[c] - self.z_list[j-1])/(self.z_list[j] - self.z_list[j-1])
                        f[c] = (
                          (1-alpha)*(1-beta)*self.xInterpolators[i-1][j-1](x[c])
                          + (1-alpha)*beta*self.xInterpolators[i-1][j](x[c])
                          + alpha*(1-beta)*self.xInterpolators[i][j-1](x[c])
                          + alpha*beta*self.xInterpolators[i][j](x[c]))
        return f
        
    def _derX(self,x,y,z):
        '''
        Returns the derivative with respect to x of the interpolated function
        at each value in x,y,z. Only called internally by HARKinterpolator3D.derivativeX.
        '''
        if _isscalar(x):
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
            beta = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            dfdx = ((1-alpha)*(1-beta)*self.xInterpolators[y_pos-1][z_pos-1]._der(x)
              + (1-alpha)*beta*self.xInterpolators[y_pos-1][z_pos]._der(x)
              + alpha*(1-beta)*self.xInterpolators[y_pos][z_pos-1]._der(x)
              + alpha*beta*self.xInterpolators[y_pos][z_pos]._der(x))              
        else:
            m = len(x)
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdx = np.zeros(m) + np.nan
            for i in xrange(1,self.y_n):
                for j in xrange(1,self.z_n):
                    c = np.logical_and(i == y_pos, j == z_pos)
                    if np.any(c):
                        alpha = (y[c] - self.y_list[i-1])/(self.y_list[i] - self.y_list[i-1])
                        beta = (z[c] - self.z_list[j-1])/(self.z_list[j] - self.z_list[j-1])
                        dfdx[c] = (
                          (1-alpha)*(1-beta)*self.xInterpolators[i-1][j-1]._der(x[c])
                          + (1-alpha)*beta*self.xInterpolators[i-1][j]._der(x[c])
                          + alpha*(1-beta)*self.xInterpolators[i][j-1]._der(x[c])
                          + alpha*beta*self.xInterpolators[i][j]._der(x[c]))
        return dfdx
        
    def _derY(self,x,y,z):
        '''
        Returns the derivative with respect to y of the interpolated function
        at each value in x,y,z. Only called internally by HARKinterpolator3D.derivativeY.
        '''
        if _isscalar(x):
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            beta = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            dfdy = (((1-beta)*self.xInterpolators[y_pos][z_pos-1](x) + beta*self.xInterpolators[y_pos][z_pos](x))
                 -  ((1-beta)*self.xInterpolators[y_pos-1][z_pos-1](x) + beta*self.xInterpolators[y_pos-1][z_pos](x)))/(self.y_list[y_pos] - self.y_list[y_pos-1])
        else:
            m = len(x)
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdy = np.zeros(m) + np.nan
            for i in xrange(1,self.y_n):
                for j in xrange(1,self.z_n):
                    c = np.logical_and(i == y_pos, j == z_pos)
                    if np.any(c):
                        beta = (z[c] - self.z_list[j-1])/(self.z_list[j] - self.z_list[j-1])
                        dfdy[c] = (((1-beta)*self.xInterpolators[i][j-1](x[c]) + beta*self.xInterpolators[i][j](x[c]))
                                -  ((1-beta)*self.xInterpolators[i-1][j-1](x[c]) + beta*self.xInterpolators[i-1][j](x[c])))/(self.y_list[i] - self.y_list[i-1])
        return dfdy
        
    def _derZ(self,x,y,z):
        '''
        Returns the derivative with respect to z of the interpolated function
        at each value in x,y,z. Only called internally by HARKinterpolator3D.derivativeZ.
        '''
        if _isscalar(x):
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
            dfdz = (((1-alpha)*self.xInterpolators[y_pos-1][z_pos](x) + alpha*self.xInterpolators[y_pos][z_pos](x))
                 -  ((1-alpha)*self.xInterpolators[y_pos-1][z_pos-1](x) + alpha*self.xInterpolators[y_pos][z_pos-1](x)))/(self.z_list[z_pos] - self.z_list[z_pos-1])
        else:
            m = len(x)
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdz = np.zeros(m) + np.nan
            for i in xrange(1,self.y_n):
                for j in xrange(1,self.z_n):
                    c = np.logical_and(i == y_pos, j == z_pos)
                    if np.any(c):
                        alpha = (y[c] - self.y_list[i-1])/(self.y_list[i] - self.y_list[i-1])
                        dfdz[c] = (((1-alpha)*self.xInterpolators[i-1][j](x[c]) + alpha*self.xInterpolators[i][j](x[c]))
                                -  ((1-alpha)*self.xInterpolators[i-1][j-1](x[c]) + alpha*self.xInterpolators[i][j-1](x[c])))/(self.z_list[j] - self.z_list[j-1])
        return dfdz

             

class TrilinearInterpOnInterp1D(HARKinterpolator4D):
    '''
    A 4D interpolator that trilinearly interpolates among a list of lists of 1D interpolators.
    '''
    distance_criteria = ['wInterpolators','x_list','y_list','z_list']
    
    def __init__(self,wInterpolators,x_values,y_values,z_values):
        '''
        Constructor for the class, generating an approximation to a function of
        the form f(w,x,y,z) using interpolations over f(w,x_0,y_0,z_0) for a fixed
        grid of y_0 and z_0 values.
        
        Parameters
        ----------
        wInterpolators : [[[HARKinterpolator1D]]]
            A list of lists of lists of 1D interpolations over the x variable.
            The i,j,k-th element of wInterpolators represents f(w,x_values[i],y_values[j],z_values[k]).
        x_values: numpy.array
            An array of x values equal in length to wInterpolators.
        y_values: numpy.array
            An array of y values equal in length to wInterpolators[0].
        z_values: numpy.array
            An array of z values equal in length to wInterpolators[0][0]
        
        Returns
        -------
        new instance of TrilinearInterpOnInterp1D
        '''
        self.wInterpolators = wInterpolators
        self.x_list = x_values
        self.x_n = x_values.size
        self.y_list = y_values
        self.y_n = y_values.size
        self.z_list = z_values
        self.z_n = z_values.size

    def _evaluate(self,w,x,y,z):
        '''
        Returns the level of the interpolated function at each value in w,x,y,z.
        Only called internally by HARKinterpolator4D.__call__ (etc).
        '''
        if _isscalar(w):
            x_pos = max(min(np.searchsorted(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (x - self.x_list[x_pos-1])/(self.x_list[x_pos] - self.x_list[x_pos-1])
            beta = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
            gamma = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            f = (
                (1-alpha)*(1-beta)*(1-gamma)*self.wInterpolators[x_pos-1][y_pos-1][z_pos-1](w)
              + (1-alpha)*(1-beta)*gamma*self.wInterpolators[x_pos-1][y_pos-1][z_pos](w)
              + (1-alpha)*beta*(1-gamma)*self.wInterpolators[x_pos-1][y_pos][z_pos-1](w)
              + (1-alpha)*beta*gamma*self.wInterpolators[x_pos-1][y_pos][z_pos](w)
              + alpha*(1-beta)*(1-gamma)*self.wInterpolators[x_pos][y_pos-1][z_pos-1](w)
              + alpha*(1-beta)*gamma*self.wInterpolators[x_pos][y_pos-1][z_pos](w)
              + alpha*beta*(1-gamma)*self.wInterpolators[x_pos][y_pos][z_pos-1](w)
              + alpha*beta*gamma*self.wInterpolators[x_pos][y_pos][z_pos](w))
        else:
            m = len(x)
            x_pos = np.searchsorted(self.x_list,x)
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            f = np.zeros(m) + np.nan
            for i in xrange(1,self.x_n):
                for j in xrange(1,self.y_n):
                    for k in xrange(1,self.z_n):
                        c = np.logical_and(np.logical_and(i == x_pos, j == y_pos),k == z_pos)
                        if np.any(c):
                            alpha = (x[c] - self.x_list[i-1])/(self.x_list[i] - self.x_list[i-1])
                            beta = (y[c] - self.y_list[j-1])/(self.y_list[j] - self.y_list[j-1])
                            gamma = (z[c] - self.z_list[k-1])/(self.z_list[k] - self.z_list[k-1])
                            f[c] = (
                                (1-alpha)*(1-beta)*(1-gamma)*self.wInterpolators[i-1][j-1][k-1](w[c])
                              + (1-alpha)*(1-beta)*gamma*self.wInterpolators[i-1][j-1][k](w[c])
                              + (1-alpha)*beta*(1-gamma)*self.wInterpolators[i-1][j][k-1](w[c])
                              + (1-alpha)*beta*gamma*self.wInterpolators[i-1][j][k](w[c])
                              + alpha*(1-beta)*(1-gamma)*self.wInterpolators[i][j-1][k-1](w[c])
                              + alpha*(1-beta)*gamma*self.wInterpolators[i][j-1][k](w[c])
                              + alpha*beta*(1-gamma)*self.wInterpolators[i][j][k-1](w[c])
                              + alpha*beta*gamma*self.wInterpolators[i][j][k](w[c]))
        return f
        
    def _derW(self,w,x,y,z):
        '''
        Returns the derivative with respect to w of the interpolated function
        at each value in w,x,y,z. Only called internally by HARKinterpolator4D.derivativeW.
        '''
        if _isscalar(w):
            x_pos = max(min(np.searchsorted(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (x - self.x_list[x_pos-1])/(self.x_list[x_pos] - self.x_list[x_pos-1])
            beta = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
            gamma = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            dfdw = (
                (1-alpha)*(1-beta)*(1-gamma)*self.wInterpolators[x_pos-1][y_pos-1][z_pos-1]._der(w)
              + (1-alpha)*(1-beta)*gamma*self.wInterpolators[x_pos-1][y_pos-1][z_pos]._der(w)
              + (1-alpha)*beta*(1-gamma)*self.wInterpolators[x_pos-1][y_pos][z_pos-1]._der(w)
              + (1-alpha)*beta*gamma*self.wInterpolators[x_pos-1][y_pos][z_pos]._der(w)
              + alpha*(1-beta)*(1-gamma)*self.wInterpolators[x_pos][y_pos-1][z_pos-1]._der(w)
              + alpha*(1-beta)*gamma*self.wInterpolators[x_pos][y_pos-1][z_pos]._der(w)
              + alpha*beta*(1-gamma)*self.wInterpolators[x_pos][y_pos][z_pos-1]._der(w)
              + alpha*beta*gamma*self.wInterpolators[x_pos][y_pos][z_pos]._der(w))
        else:
            m = len(x)
            x_pos = np.searchsorted(self.x_list,x)
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdw = np.zeros(m) + np.nan
            for i in xrange(1,self.x_n):
                for j in xrange(1,self.y_n):
                    for k in xrange(1,self.z_n):
                        c = np.logical_and(np.logical_and(i == x_pos, j == y_pos),k == z_pos)
                        if np.any(c):
                            alpha = (x[c] - self.x_list[i-1])/(self.x_list[i] - self.x_list[i-1])
                            beta = (y[c] - self.y_list[j-1])/(self.y_list[j] - self.y_list[j-1])
                            gamma = (z[c] - self.z_list[k-1])/(self.z_list[k] - self.z_list[k-1])
                            dfdw[c] = (
                                (1-alpha)*(1-beta)*(1-gamma)*self.wInterpolators[i-1][j-1][k-1]._der(w[c])
                              + (1-alpha)*(1-beta)*gamma*self.wInterpolators[i-1][j-1][k]._der(w[c])
                              + (1-alpha)*beta*(1-gamma)*self.wInterpolators[i-1][j][k-1]._der(w[c])
                              + (1-alpha)*beta*gamma*self.wInterpolators[i-1][j][k]._der(w[c])
                              + alpha*(1-beta)*(1-gamma)*self.wInterpolators[i][j-1][k-1]._der(w[c])
                              + alpha*(1-beta)*gamma*self.wInterpolators[i][j-1][k]._der(w[c])
                              + alpha*beta*(1-gamma)*self.wInterpolators[i][j][k-1]._der(w[c])
                              + alpha*beta*gamma*self.wInterpolators[i][j][k]._der(w[c]))
        return dfdw
        
    def _derX(self,w,x,y,z):
        '''
        Returns the derivative with respect to x of the interpolated function
        at each value in w,x,y,z. Only called internally by HARKinterpolator4D.derivativeX.
        '''
        if _isscalar(w):
            x_pos = max(min(np.searchsorted(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            beta = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
            gamma = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            dfdx = (
             ((1-beta)*(1-gamma)*self.wInterpolators[x_pos][y_pos-1][z_pos-1](w)
              + (1-beta)*gamma*self.wInterpolators[x_pos][y_pos-1][z_pos](w)
              + beta*(1-gamma)*self.wInterpolators[x_pos][y_pos][z_pos-1](w)
              + beta*gamma*self.wInterpolators[x_pos][y_pos][z_pos](w)) - 
              ((1-beta)*(1-gamma)*self.wInterpolators[x_pos-1][y_pos-1][z_pos-1](w)
              + (1-beta)*gamma*self.wInterpolators[x_pos-1][y_pos-1][z_pos](w)
              + beta*(1-gamma)*self.wInterpolators[x_pos-1][y_pos][z_pos-1](w)
              + beta*gamma*self.wInterpolators[x_pos-1][y_pos][z_pos](w)))/(self.x_list[x_pos] - self.x_list[x_pos-1])
        else:
            m = len(x)
            x_pos = np.searchsorted(self.x_list,x)
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdx = np.zeros(m) + np.nan
            for i in xrange(1,self.x_n):
                for j in xrange(1,self.y_n):
                    for k in xrange(1,self.z_n):
                        c = np.logical_and(np.logical_and(i == x_pos, j == y_pos),k == z_pos)
                        if np.any(c):
                            beta = (y[c] - self.y_list[j-1])/(self.y_list[j] - self.y_list[j-1])
                            gamma = (z[c] - self.z_list[k-1])/(self.z_list[k] - self.z_list[k-1])
                            dfdx[c] = (
                              ((1-beta)*(1-gamma)*self.wInterpolators[i][j-1][k-1](w[c])
                            + (1-beta)*gamma*self.wInterpolators[i][j-1][k](w[c])
                            + beta*(1-gamma)*self.wInterpolators[i][j][k-1](w[c])
                            + beta*gamma*self.wInterpolators[i][j][k](w[c])) - 
                             ((1-beta)*(1-gamma)*self.wInterpolators[i-1][j-1][k-1](w[c])
                            + (1-beta)*gamma*self.wInterpolators[i-1][j-1][k](w[c])
                            + beta*(1-gamma)*self.wInterpolators[i-1][j][k-1](w[c])
                            + beta*gamma*self.wInterpolators[i-1][j][k](w[c])))/(self.x_list[i] - self.x_list[i-1])
        return dfdx
        
    def _derY(self,w,x,y,z):
        '''
        Returns the derivative with respect to y of the interpolated function
        at each value in w,x,y,z. Only called internally by HARKinterpolator4D.derivativeY.
        '''
        if _isscalar(w):
            x_pos = max(min(np.searchsorted(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (x - self.x_list[x_pos-1])/(self.y_list[x_pos] - self.x_list[x_pos-1])
            gamma = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            dfdy = (
             ((1-alpha)*(1-gamma)*self.wInterpolators[x_pos-1][y_pos][z_pos-1](w)
              + (1-alpha)*gamma*self.wInterpolators[x_pos-1][y_pos][z_pos](w)
              + alpha*(1-gamma)*self.wInterpolators[x_pos][y_pos][z_pos-1](w)
              + alpha*gamma*self.wInterpolators[x_pos][y_pos][z_pos](w)) - 
              ((1-alpha)*(1-gamma)*self.wInterpolators[x_pos-1][y_pos-1][z_pos-1](w)
              + (1-alpha)*gamma*self.wInterpolators[x_pos-1][y_pos-1][z_pos](w)
              + alpha*(1-gamma)*self.wInterpolators[x_pos][y_pos-1][z_pos-1](w)
              + alpha*gamma*self.wInterpolators[x_pos][y_pos-1][z_pos](w)))/(self.y_list[y_pos] - self.y_list[y_pos-1])
        else:
            m = len(x)
            x_pos = np.searchsorted(self.x_list,x)
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdy = np.zeros(m) + np.nan
            for i in xrange(1,self.x_n):
                for j in xrange(1,self.y_n):
                    for k in xrange(1,self.z_n):
                        c = np.logical_and(np.logical_and(i == x_pos, j == y_pos),k == z_pos)
                        if np.any(c):
                            alpha = (x[c] - self.x_list[i-1])/(self.x_list[i] - self.x_list[i-1])
                            gamma = (z[c] - self.z_list[k-1])/(self.z_list[k] - self.z_list[k-1])
                            dfdy[c] = (
                                  ((1-alpha)*(1-gamma)*self.wInterpolators[i-1][j][k-1](w[c])
                                 + (1-alpha)*gamma*self.wInterpolators[i-1][j][k](w[c])
                                 + alpha*(1-gamma)*self.wInterpolators[i][j][k-1](w[c])
                                 + alpha*gamma*self.wInterpolators[i][j][k](w[c])) - 
                                  ((1-alpha)*(1-gamma)*self.wInterpolators[i-1][j-1][k-1](w[c])
                                 + (1-alpha)*gamma*self.wInterpolators[i-1][j-1][k](w[c])
                                 + alpha*(1-gamma)*self.wInterpolators[i][j-1][k-1](w[c])
                                 + alpha*gamma*self.wInterpolators[i][j-1][k](w[c])))/(self.y_list[j] - self.y_list[j-1])
        return dfdy
        
    def _derZ(self,w,x,y,z):
        '''
        Returns the derivative with respect to z of the interpolated function
        at each value in w,x,y,z. Only called internally by HARKinterpolator4D.derivativeZ.
        '''
        if _isscalar(w):
            x_pos = max(min(np.searchsorted(self.x_list,x),self.x_n-1),1)
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (x - self.x_list[x_pos-1])/(self.y_list[x_pos] - self.x_list[x_pos-1])
            beta = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
            dfdz = (
             ((1-alpha)*(1-beta)*self.wInterpolators[x_pos-1][y_pos-1][z_pos](w)
              + (1-alpha)*beta*self.wInterpolators[x_pos-1][y_pos][z_pos](w)
              + alpha*(1-beta)*self.wInterpolators[x_pos][y_pos-1][z_pos](w)
              + alpha*beta*self.wInterpolators[x_pos][y_pos][z_pos](w)) - 
              ((1-alpha)*(1-beta)*self.wInterpolators[x_pos-1][y_pos-1][z_pos-1](w)
              + (1-alpha)*beta*self.wInterpolators[x_pos-1][y_pos][z_pos-1](w)
              + alpha*(1-beta)*self.wInterpolators[x_pos][y_pos-1][z_pos-1](w)
              + alpha*beta*self.wInterpolators[x_pos][y_pos][z_pos-1](w)))/(self.z_list[z_pos] - self.z_list[z_pos-1])
        else:
            m = len(x)
            x_pos = np.searchsorted(self.x_list,x)
            x_pos[x_pos > self.x_n-1] = self.x_n-1
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdz = np.zeros(m) + np.nan
            for i in xrange(1,self.x_n):
                for j in xrange(1,self.y_n):
                    for k in xrange(1,self.z_n):
                        c = np.logical_and(np.logical_and(i == x_pos, j == y_pos),k == z_pos)
                        if np.any(c):
                            alpha = (x[c] - self.x_list[i-1])/(self.x_list[i] - self.x_list[i-1])
                            beta = (y[c] - self.y_list[j-1])/(self.y_list[j] - self.y_list[j-1])
                            dfdz[c] = (
                                  ((1-alpha)*(1-beta)*self.wInterpolators[i-1][j-1][k](w[c])
                                 + (1-alpha)*beta*self.wInterpolators[i-1][j][k](w[c])
                                 + alpha*(1-beta)*self.wInterpolators[i][j-1][k](w[c])
                                 + alpha*beta*self.wInterpolators[i][j][k](w[c])) - 
                                  ((1-alpha)*(1-beta)*self.wInterpolators[i-1][j-1][k-1](w[c])
                                 + (1-alpha)*beta*self.wInterpolators[i-1][j][k-1](w[c])
                                 + alpha*(1-beta)*self.wInterpolators[i][j-1][k-1](w[c])
                                 + alpha*beta*self.wInterpolators[i][j][k-1](w[c])))/(self.z_list[k] - self.z_list[k-1])
        return dfdz
        
       
class LinearInterpOnInterp2D(HARKinterpolator3D):
    '''
    A 3D interpolation method that linearly interpolates between "layers" of
    arbitrary 2D interpolations.  Useful for models with two endogenous state
    variables and one exogenous state variable when solving with the endogenous
    grid method.  NOTE: should not be used if an exogenous 3D grid is used, will
    be significantly slower than TrilinearInterp.
    '''
    distance_criteria = ['xyInterpolators','z_list']

    def __init__(self,xyInterpolators,z_values):
        '''
        Constructor for the class, generating an approximation to a function of
        the form f(x,y,z) using interpolations over f(x,y,z_0) for a fixed grid
        of z_0 values.
        
        Parameters
        ----------
        xyInterpolators : [HARKinterpolator2D]
            A list of 2D interpolations over the x and y variables.  The nth
            element of xyInterpolators represents f(x,y,z_values[n]).
        z_values: numpy.array
            An array of z values equal in length to xyInterpolators.
            
        Returns
        -------
        new instance of LinearInterpOnInterp2D
        '''
        self.xyInterpolators = xyInterpolators
        self.z_list = z_values
        self.z_n = z_values.size
        
    def _evaluate(self,x,y,z):
        '''
        Returns the level of the interpolated function at each value in x,y,z.
        Only called internally by HARKinterpolator3D.__call__ (etc).
        '''
        if _isscalar(x):
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            f = (1-alpha)*self.xyInterpolators[z_pos-1](x,y) + alpha*self.xyInterpolators[z_pos](x,y)
        else:
            m = len(x)
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            f = np.zeros(m) + np.nan
            if x.size > 0:
                for i in xrange(1,self.z_n):
                    c = z_pos == i
                    if np.any(c):
                        alpha = (z[c] - self.z_list[i-1])/(self.z_list[i] - self.z_list[i-1])
                        f[c] = (1-alpha)*self.xyInterpolators[i-1](x[c],y[c]) + alpha*self.xyInterpolators[i](x[c],y[c]) 
        return f
        
    def _derX(self,x,y,z):
        '''
        Returns the derivative with respect to x of the interpolated function
        at each value in x,y,z. Only called internally by HARKinterpolator3D.derivativeX.
        '''
        if _isscalar(x):
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            dfdx = (1-alpha)*self.xyInterpolators[z_pos-1].derivativeX(x,y) + alpha*self.xyInterpolators[z_pos].derivativeX(x,y)
        else:
            m = len(x)
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdx = np.zeros(m) + np.nan
            if x.size > 0:
                for i in xrange(1,self.z_n):
                    c = z_pos == i
                    if np.any(c):
                        alpha = (z[c] - self.z_list[i-1])/(self.z_list[i] - self.z_list[i-1])
                        dfdx[c] = (1-alpha)*self.xyInterpolators[i-1].derivativeX(x[c],y[c]) + alpha*self.xyInterpolators[i].derivativeX(x[c],y[c]) 
        return dfdx
        
    def _derY(self,x,y,z):
        '''
        Returns the derivative with respect to y of the interpolated function
        at each value in x,y,z. Only called internally by HARKinterpolator3D.derivativeY.
        '''
        if _isscalar(x):
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            dfdy = (1-alpha)*self.xyInterpolators[z_pos-1].derivativeY(x,y) + alpha*self.xyInterpolators[z_pos].derivativeY(x,y)
        else:
            m = len(x)
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdy = np.zeros(m) + np.nan
            if x.size > 0:
                for i in xrange(1,self.z_n):
                    c = z_pos == i
                    if np.any(c):
                        alpha = (z[c] - self.z_list[i-1])/(self.z_list[i] - self.z_list[i-1])
                        dfdy[c] = (1-alpha)*self.xyInterpolators[i-1].derivativeY(x[c],y[c]) + alpha*self.xyInterpolators[i].derivativeY(x[c],y[c]) 
        return dfdy
        
    def _derZ(self,x,y,z):
        '''
        Returns the derivative with respect to z of the interpolated function
        at each value in x,y,z. Only called internally by HARKinterpolator3D.derivativeZ.
        '''
        if _isscalar(x):
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            dfdz = (self.xyInterpolators[z_pos].derivativeX(x,y) - self.xyInterpolators[z_pos-1].derivativeX(x,y))/(self.z_list[z_pos] - self.z_list[z_pos-1])
        else:
            m = len(x)
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdz = np.zeros(m) + np.nan
            if x.size > 0:
                for i in xrange(1,self.z_n):
                    c = z_pos == i
                    if np.any(c):
                        dfdz[c] = (self.xyInterpolators[i](x[c],y[c]) - self.xyInterpolators[i-1](x[c],y[c]))/(self.z_list[i] - self.z_list[i-1])
        return dfdz

class BilinearInterpOnInterp2D(HARKinterpolator4D):
    '''
    A 4D interpolation method that bilinearly interpolates among "layers" of
    arbitrary 2D interpolations.  Useful for models with two endogenous state
    variables and two exogenous state variables when solving with the endogenous
    grid method.  NOTE: should not be used if an exogenous 4D grid is used, will
    be significantly slower than QuadlinearInterp.
    '''
    distance_criteria = ['wxInterpolators','y_list','z_list']
    
    def __init__(self,wxInterpolators,y_values,z_values):
        '''
        Constructor for the class, generating an approximation to a function of
        the form f(w,x,y,z) using interpolations over f(w,x,y_0,z_0) for a fixed
        grid of y_0 and z_0 values.
        
        Parameters
        ----------
        wxInterpolators : [[HARKinterpolator2D]]
            A list of lists of 2D interpolations over the w and x variables.
            The i,j-th element of wxInterpolators represents
            f(w,x,y_values[i],z_values[j]).
        y_values: numpy.array
            An array of y values equal in length to wxInterpolators.
        z_values: numpy.array
            An array of z values equal in length to wxInterpolators[0].
            
        Returns
        -------
        new instance of BilinearInterpOnInterp2D
        '''
        self.wxInterpolators = wxInterpolators
        self.y_list = y_values
        self.y_n = y_values.size
        self.z_list = z_values
        self.z_n = z_values.size
        
    def _evaluate(self,w,x,y,z):
        '''
        Returns the level of the interpolated function at each value in x,y,z.
        Only called internally by HARKinterpolator4D.__call__ (etc).
        '''
        if _isscalar(x):
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
            beta = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            f = ((1-alpha)*(1-beta)*self.wxInterpolators[y_pos-1][z_pos-1](w,x)
              + (1-alpha)*beta*self.wxInterpolators[y_pos-1][z_pos](w,x)
              + alpha*(1-beta)*self.wxInterpolators[y_pos][z_pos-1](w,x)
              + alpha*beta*self.wxInterpolators[y_pos][z_pos](w,x))              
        else:
            m = len(x)
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            f = np.zeros(m) + np.nan
            for i in xrange(1,self.y_n):
                for j in xrange(1,self.z_n):
                    c = np.logical_and(i == y_pos, j == z_pos)
                    if np.any(c):
                        alpha = (y[c] - self.y_list[i-1])/(self.y_list[i] - self.y_list[i-1])
                        beta = (z[c] - self.z_list[j-1])/(self.z_list[j] - self.z_list[j-1])
                        f[c] = (
                          (1-alpha)*(1-beta)*self.wxInterpolators[i-1][j-1](w[c],x[c])
                          + (1-alpha)*beta*self.wxInterpolators[i-1][j](w[c],x[c])
                          + alpha*(1-beta)*self.wxInterpolators[i][j-1](w[c],x[c])
                          + alpha*beta*self.wxInterpolators[i][j](w[c],x[c]))
        return f
        
    def _derW(self,w,x,y,z):
        '''
        Returns the derivative with respect to w of the interpolated function
        at each value in w,x,y,z. Only called internally by HARKinterpolator4D.derivativeW.
        '''
        # This may look strange, as we call the derivativeX() method to get the
        # derivative with respect to w, but that's just a quirk of 4D interpolations
        # beginning with w rather than x.  The derivative wrt the first dimension
        # of an element of wxInterpolators is the w-derivative of the main function.
        if _isscalar(x):
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
            beta = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            dfdw = ((1-alpha)*(1-beta)*self.wxInterpolators[y_pos-1][z_pos-1].derivativeX(w,x)
              + (1-alpha)*beta*self.wxInterpolators[y_pos-1][z_pos].derivativeX(w,x)
              + alpha*(1-beta)*self.wxInterpolators[y_pos][z_pos-1].derivativeX(w,x)
              + alpha*beta*self.wxInterpolators[y_pos][z_pos].derivativeX(w,x))              
        else:
            m = len(x)
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdw = np.zeros(m) + np.nan
            for i in xrange(1,self.y_n):
                for j in xrange(1,self.z_n):
                    c = np.logical_and(i == y_pos, j == z_pos)
                    if np.any(c):
                        alpha = (y[c] - self.y_list[i-1])/(self.y_list[i] - self.y_list[i-1])
                        beta = (z[c] - self.z_list[j-1])/(self.z_list[j] - self.z_list[j-1])
                        dfdw[c] = (
                          (1-alpha)*(1-beta)*self.wxInterpolators[i-1][j-1].derivativeX(w[c],x[c])
                          + (1-alpha)*beta*self.wxInterpolators[i-1][j].derivativeX(w[c],x[c])
                          + alpha*(1-beta)*self.wxInterpolators[i][j-1].derivativeX(w[c],x[c])
                          + alpha*beta*self.wxInterpolators[i][j].derivativeX(w[c],x[c]))
        return dfdw
        
    def _derX(self,w,x,y,z):
        '''
        Returns the derivative with respect to x of the interpolated function
        at each value in w,x,y,z. Only called internally by HARKinterpolator4D.derivativeX.
        '''
        # This may look strange, as we call the derivativeY() method to get the
        # derivative with respect to x, but that's just a quirk of 4D interpolations
        # beginning with w rather than x.  The derivative wrt the second dimension
        # of an element of wxInterpolators is the x-derivative of the main function.
        if _isscalar(x):
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
            beta = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            dfdx = ((1-alpha)*(1-beta)*self.wxInterpolators[y_pos-1][z_pos-1].derivativeY(w,x)
              + (1-alpha)*beta*self.wxInterpolators[y_pos-1][z_pos].derivativeY(w,x)
              + alpha*(1-beta)*self.wxInterpolators[y_pos][z_pos-1].derivativeY(w,x)
              + alpha*beta*self.wxInterpolators[y_pos][z_pos].derivativeY(w,x))              
        else:
            m = len(x)
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdx = np.zeros(m) + np.nan
            for i in xrange(1,self.y_n):
                for j in xrange(1,self.z_n):
                    c = np.logical_and(i == y_pos, j == z_pos)
                    if np.any(c):
                        alpha = (y[c] - self.y_list[i-1])/(self.y_list[i] - self.y_list[i-1])
                        beta = (z[c] - self.z_list[j-1])/(self.z_list[j] - self.z_list[j-1])
                        dfdx[c] = (
                          (1-alpha)*(1-beta)*self.wxInterpolators[i-1][j-1].derivativeY(w[c],x[c])
                          + (1-alpha)*beta*self.wxInterpolators[i-1][j].derivativeY(w[c],x[c])
                          + alpha*(1-beta)*self.wxInterpolators[i][j-1].derivativeY(w[c],x[c])
                          + alpha*beta*self.wxInterpolators[i][j].derivativeY(w[c],x[c]))
        return dfdx
        
    def _derY(self,w,x,y,z):
        '''
        Returns the derivative with respect to y of the interpolated function
        at each value in w,x,y,z. Only called internally by HARKinterpolator4D.derivativeY.
        '''
        if _isscalar(x):
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            beta = (z - self.z_list[z_pos-1])/(self.z_list[z_pos] - self.z_list[z_pos-1])
            dfdy = (((1-beta)*self.wxInterpolators[y_pos][z_pos-1](w,x) + beta*self.wxInterpolators[y_pos][z_pos](w,x))
                 -  ((1-beta)*self.wxInterpolators[y_pos-1][z_pos-1](w,x) + beta*self.wxInterpolators[y_pos-1][z_pos](w,x)))/(self.y_list[y_pos] - self.y_list[y_pos-1])
        else:
            m = len(x)
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdy = np.zeros(m) + np.nan
            for i in xrange(1,self.y_n):
                for j in xrange(1,self.z_n):
                    c = np.logical_and(i == y_pos, j == z_pos)
                    if np.any(c):
                        beta = (z[c] - self.z_list[j-1])/(self.z_list[j] - self.z_list[j-1])
                        dfdy[c] = (((1-beta)*self.wxInterpolators[i][j-1](w[c],x[c]) + beta*self.wxInterpolators[i][j](w[c],x[c]))
                                -  ((1-beta)*self.wxInterpolators[i-1][j-1](w[c],x[c]) + beta*self.wxInterpolators[i-1][j](w[c],x[c])))/(self.y_list[i] - self.y_list[i-1])
        return dfdy
        
    def _derZ(self,w,x,y,z):
        '''
        Returns the derivative with respect to z of the interpolated function
        at each value in w,x,y,z. Only called internally by HARKinterpolator4D.derivativeZ.
        '''
        if _isscalar(x):
            y_pos = max(min(np.searchsorted(self.y_list,y),self.y_n-1),1)
            z_pos = max(min(np.searchsorted(self.z_list,z),self.z_n-1),1)
            alpha = (y - self.y_list[y_pos-1])/(self.y_list[y_pos] - self.y_list[y_pos-1])
            dfdz = (((1-alpha)*self.wxInterpolators[y_pos-1][z_pos](w,x) + alpha*self.wxInterpolators[y_pos][z_pos](w,x))
                 -  ((1-alpha)*self.wxInterpolators[y_pos-1][z_pos-1](w,x) + alpha*self.wxInterpolators[y_pos][z_pos-1](w,x)))/(self.z_list[z_pos] - self.z_list[z_pos-1])
        else:
            m = len(x)
            y_pos = np.searchsorted(self.y_list,y)
            y_pos[y_pos > self.y_n-1] = self.y_n-1
            y_pos[y_pos < 1] = 1
            z_pos = np.searchsorted(self.z_list,z)
            z_pos[z_pos > self.z_n-1] = self.z_n-1
            z_pos[z_pos < 1] = 1
            dfdz = np.zeros(m) + np.nan
            for i in xrange(1,self.y_n):
                for j in xrange(1,self.z_n):
                    c = np.logical_and(i == y_pos, j == z_pos)
                    if np.any(c):
                        alpha = (y[c] - self.y_list[i-1])/(self.y_list[i] - self.y_list[i-1])
                        dfdz[c] = (((1-alpha)*self.wxInterpolators[i-1][j](w[c],x[c]) + alpha*self.wxInterpolators[i][j](w[c],x[c]))
                                -  ((1-alpha)*self.wxInterpolators[i-1][j-1](w[c],x[c]) + alpha*self.wxInterpolators[i][j-1](w[c],x[c])))/(self.z_list[j] - self.z_list[j-1])
        return dfdz
        
        
class Curvilinear2DInterp(HARKinterpolator2D):
    '''
    A 2D interpolation method for curvilinear or "warped grid" interpolation, as
    in White (2015).  Used for models with two endogenous states that are solved
    with the endogenous grid method.
    '''
    distance_criteria = ['f_values','x_values','y_values']
    
    def __init__(self,f_values,x_values,y_values):
        '''
        Constructor for 2D curvilinear interpolation for a function f(x,y)
        
        Parameters
        ----------
        f_values: numpy.array
            A 2D array of function values such that f_values[i,j] =
            f(x_values[i,j],y_values[i,j]).
        x_values: numpy.array
            A 2D array of x values of the same size as f_values.
        y_values: numpy.array
            A 2D array of y values of the same size as f_values.
            
        Returns
        -------
        new instance of Curvilinear2DInterp
        '''
        self.f_values = f_values
        self.x_values = x_values
        self.y_values = y_values
        my_shape = f_values.shape
        self.x_n = my_shape[0]
        self.y_n = my_shape[1]
        self.updatePolarity()
        
    def updatePolarity(self):
        '''
        Fills in the polarity attribute of the interpolation, determining whether
        the "plus" (True) or "minus" (False) solution of the system of equations
        should be used for each sector.  Needs to be called in __init__.
        
        Parameters
        ----------
        none
            
        Returns
        -------
        none
        '''       
        # Grab a point known to be inside each sector: the midway point between
        # the lower left and upper right vertex of each sector
        x_temp = 0.5*(self.x_values[0:(self.x_n-1),0:(self.y_n-1)] + self.x_values[1:self.x_n,1:self.y_n])
        y_temp = 0.5*(self.y_values[0:(self.x_n-1),0:(self.y_n-1)] + self.y_values[1:self.x_n,1:self.y_n])
        size = (self.x_n-1)*(self.y_n-1)
        x_temp = np.reshape(x_temp,size)
        y_temp = np.reshape(y_temp,size)
        y_pos = np.tile(np.arange(0,self.y_n-1),self.x_n-1)
        x_pos = np.reshape(np.tile(np.arange(0,self.x_n-1),(self.y_n-1,1)).transpose(),size)
        
        # Set the polarity of all sectors to "plus", then test each sector
        self.polarity = np.ones((self.x_n-1,self.y_n-1),dtype=bool)
        alpha, beta = self.findCoords(x_temp,y_temp,x_pos,y_pos)
        polarity = np.logical_and(
            np.logical_and(alpha > 0, alpha < 1),
            np.logical_and(beta > 0, beta < 1))
        
        # Update polarity: if (alpha,beta) not in the unit square, then that
        # sector must use the "minus" solution instead
        self.polarity = np.reshape(polarity,(self.x_n-1,self.y_n-1))
        
    def findSector(self,x,y):
        '''
        Finds the quadrilateral "sector" for each (x,y) point in the input.
        Only called as a subroutine of _evaluate().
        
        Parameters
        ----------
        x : np.array
            Values whose sector should be found.
        y : np.array
            Values whose sector should be found.  Should be same size as x.
            
        Returns
        -------
        x_pos : np.array
            Sector x-coordinates for each point of the input, of the same size.
        y_pos : np.array
            Sector y-coordinates for each point of the input, of the same size.
        '''
        # Initialize the sector guess
        m = x.size
        x_pos_guess = (np.ones(m)*self.x_n/2).astype(int)
        y_pos_guess = (np.ones(m)*self.y_n/2).astype(int)
        
        # Define a function that checks whether a set of points violates a linear
        # boundary defined by (x_bound_1,y_bound_1) and (x_bound_2,y_bound_2),
        # where the latter is *COUNTER CLOCKWISE* from the former.  Returns
        # 1 if the point is outside the boundary and 0 otherwise.
        violationCheck = lambda x_check,y_check,x_bound_1,y_bound_1,x_bound_2,y_bound_2 : (
            (y_bound_2 - y_bound_1)*x_check - (x_bound_2 - x_bound_1)*y_check > x_bound_1*y_bound_2 - y_bound_1*x_bound_2 ) + 0
        
        # Identify the correct sector for each point to be evaluated
        these = np.ones(m,dtype=bool)
        max_loops = self.x_n + self.y_n
        loops = 0
        while np.any(these) and loops < max_loops:
            # Get coordinates for the four vertices: (xA,yA),...,(xD,yD)
            x_temp = x[these]
            y_temp = y[these]
            xA = self.x_values[x_pos_guess[these],y_pos_guess[these]]
            xB = self.x_values[x_pos_guess[these]+1,y_pos_guess[these]]
            xC = self.x_values[x_pos_guess[these],y_pos_guess[these]+1]
            xD = self.x_values[x_pos_guess[these]+1,y_pos_guess[these]+1]
            yA = self.y_values[x_pos_guess[these],y_pos_guess[these]]
            yB = self.y_values[x_pos_guess[these]+1,y_pos_guess[these]]
            yC = self.y_values[x_pos_guess[these],y_pos_guess[these]+1]
            yD = self.y_values[x_pos_guess[these]+1,y_pos_guess[these]+1]
            
            # Check the "bounding box" for the sector: is this guess plausible?
            move_down = (y_temp < np.minimum(yA,yB)) + 0
            move_right = (x_temp > np.maximum(xB,xD)) + 0
            move_up = (y_temp > np.maximum(yC,yD)) + 0
            move_left = (x_temp < np.minimum(xA,xC)) + 0
            
            # Check which boundaries are violated (and thus where to look next)
            c = (move_down + move_right + move_up + move_left) == 0
            move_down[c] = violationCheck(x_temp[c],y_temp[c],xA[c],yA[c],xB[c],yB[c])
            move_right[c] = violationCheck(x_temp[c],y_temp[c],xB[c],yB[c],xD[c],yD[c])
            move_up[c] = violationCheck(x_temp[c],y_temp[c],xD[c],yD[c],xC[c],yC[c])
            move_left[c] = violationCheck(x_temp[c],y_temp[c],xC[c],yC[c],xA[c],yA[c])
            
            # Update the sector guess based on the violations
            x_pos_next = x_pos_guess[these] - move_left + move_right
            x_pos_next[x_pos_next < 0] = 0
            x_pos_next[x_pos_next > (self.x_n-2)] = self.x_n-2
            y_pos_next = y_pos_guess[these] - move_down + move_up
            y_pos_next[y_pos_next < 0] = 0
            y_pos_next[y_pos_next > (self.y_n-2)] = self.y_n-2
            
            # Check which sectors have not changed, and mark them as complete
            no_move = np.array(np.logical_and(x_pos_guess[these] == x_pos_next, y_pos_guess[these] == y_pos_next))
            x_pos_guess[these] = x_pos_next
            y_pos_guess[these] = y_pos_next
            temp = these.nonzero()
            these[temp[0][no_move]] = False
            
            # Move to the next iteration of the search
            loops += 1
            
        # Return the output
        x_pos = x_pos_guess
        y_pos = y_pos_guess
        return x_pos, y_pos
        
    def findCoords(self,x,y,x_pos,y_pos):
        '''
        Calculates the relative coordinates (alpha,beta) for each point (x,y),
        given the sectors (x_pos,y_pos) in which they reside.  Only called as
        a subroutine of __call__().
        
        Parameters
        ----------
        x : np.array
            Values whose sector should be found.
        y : np.array
            Values whose sector should be found.  Should be same size as x.
        x_pos : np.array
            Sector x-coordinates for each point in (x,y), of the same size.
        y_pos : np.array
            Sector y-coordinates for each point in (x,y), of the same size.
            
        Returns
        -------
        alpha : np.array
            Relative "horizontal" position of the input in their respective sectors.
        beta : np.array
            Relative "vertical" position of the input in their respective sectors.
        '''
        # Calculate relative coordinates in the sector for each point
        xA = self.x_values[x_pos,y_pos]
        xB = self.x_values[x_pos+1,y_pos]
        xC = self.x_values[x_pos,y_pos+1]
        xD = self.x_values[x_pos+1,y_pos+1]
        yA = self.y_values[x_pos,y_pos]
        yB = self.y_values[x_pos+1,y_pos]
        yC = self.y_values[x_pos,y_pos+1]
        yD = self.y_values[x_pos+1,y_pos+1]
        polarity = 2.0*self.polarity[x_pos,y_pos] - 1.0
        a = xA
        b = (xB-xA)
        c = (xC-xA)
        d = (xA-xB-xC+xD)
        e = yA
        f = (yB-yA)
        g = (yC-yA)
        h = (yA-yB-yC+yD)
        denom = (d*g-h*c)
        mu = (h*b-d*f)/denom
        tau = (h*(a-x) - d*(e-y))/denom
        zeta = a - x + c*tau
        eta = b + c*mu + d*tau
        theta = d*mu
        alpha = (-eta + polarity*np.sqrt(eta**2.0 - 4.0*zeta*theta))/(2.0*theta)
        beta = mu*alpha + tau
        
        # Alternate method if there are sectors that are "too regular"
        z = np.logical_or(np.isnan(alpha),np.isnan(beta))   # These points weren't able to identify coordinates
        if np.any(z): 
            these = np.isclose(f/b,(yD-yC)/(xD-xC)) # iso-beta lines have equal slope
            if np.any(these):
                kappa     = f[these]/b[these]
                int_bot   = yA[these] - kappa*xA[these]
                int_top   = yC[these] - kappa*xC[these]
                int_these = y[these] - kappa*x[these]
                beta_temp = (int_these-int_bot)/(int_top-int_bot)
                x_left    = beta_temp*xC[these] + (1.0-beta_temp)*xA[these]
                x_right   = beta_temp*xD[these] + (1.0-beta_temp)*xB[these]
                alpha_temp= (x[these]-x_left)/(x_right-x_left)
                beta[these]  = beta_temp
                alpha[these] = alpha_temp
                
            #print(np.sum(np.isclose(g/c,(yD-yB)/(xD-xB))))
        
        return alpha, beta
        
    def _evaluate(self,x,y):
        '''
        Returns the level of the interpolated function at each value in x,y.
        Only called internally by HARKinterpolator2D.__call__ (etc).
        '''
        x_pos, y_pos = self.findSector(x,y)
        alpha, beta = self.findCoords(x,y,x_pos,y_pos)
        
        # Calculate the function at each point using bilinear interpolation
        f = (
             (1-alpha)*(1-beta)*self.f_values[x_pos,y_pos]
          +  (1-alpha)*beta*self.f_values[x_pos,y_pos+1]
          +  alpha*(1-beta)*self.f_values[x_pos+1,y_pos]
          +  alpha*beta*self.f_values[x_pos+1,y_pos+1])
        return f
        
    def _derX(self,x,y):
        '''
        Returns the derivative with respect to x of the interpolated function
        at each value in x,y. Only called internally by HARKinterpolator2D.derivativeX.
        '''
        x_pos, y_pos = self.findSector(x,y)
        alpha, beta = self.findCoords(x,y,x_pos,y_pos)
        
        # Get four corners data for each point
        xA = self.x_values[x_pos,y_pos]
        xB = self.x_values[x_pos+1,y_pos]
        xC = self.x_values[x_pos,y_pos+1]
        xD = self.x_values[x_pos+1,y_pos+1]
        yA = self.y_values[x_pos,y_pos]
        yB = self.y_values[x_pos+1,y_pos]
        yC = self.y_values[x_pos,y_pos+1]
        yD = self.y_values[x_pos+1,y_pos+1]
        fA = self.f_values[x_pos,y_pos]
        fB = self.f_values[x_pos+1,y_pos]
        fC = self.f_values[x_pos,y_pos+1]
        fD = self.f_values[x_pos+1,y_pos+1]
        
        # Calculate components of the alpha,beta --> x,y delta translation matrix
        alpha_x = (1-beta)*(xB-xA) + beta*(xD-xC)
        alpha_y = (1-beta)*(yB-yA) + beta*(yD-yC)
        beta_x  = (1-alpha)*(xC-xA) + alpha*(xD-xB)
        beta_y  = (1-alpha)*(yC-yA) + alpha*(yD-yB)
        
        # Invert the delta translation matrix into x,y --> alpha,beta
        det = alpha_x*beta_y - beta_x*alpha_y
        x_alpha = beta_y/det
        x_beta  = -alpha_y/det
        #y_alpha = -beta_x/det
        #y_beta  = alpha_x/det
        
        # Calculate the derivative of f w.r.t. alpha and beta
        dfda = (1-beta)*(fB-fA) + beta*(fD-fC)
        dfdb = (1-alpha)*(fC-fA) + alpha*(fD-fB)
        
        # Calculate the derivative with respect to x (and return it)
        dfdx = x_alpha*dfda + x_beta*dfdb
        return dfdx
        
    def _derY(self,x,y):
        '''
        Returns the derivative with respect to y of the interpolated function
        at each value in x,y. Only called internally by HARKinterpolator2D.derivativeX.
        '''
        x_pos, y_pos = self.findSector(x,y)
        alpha, beta = self.findCoords(x,y,x_pos,y_pos)
        
        # Get four corners data for each point
        xA = self.x_values[x_pos,y_pos]
        xB = self.x_values[x_pos+1,y_pos]
        xC = self.x_values[x_pos,y_pos+1]
        xD = self.x_values[x_pos+1,y_pos+1]
        yA = self.y_values[x_pos,y_pos]
        yB = self.y_values[x_pos+1,y_pos]
        yC = self.y_values[x_pos,y_pos+1]
        yD = self.y_values[x_pos+1,y_pos+1]
        fA = self.f_values[x_pos,y_pos]
        fB = self.f_values[x_pos+1,y_pos]
        fC = self.f_values[x_pos,y_pos+1]
        fD = self.f_values[x_pos+1,y_pos+1]
        
        # Calculate components of the alpha,beta --> x,y delta translation matrix
        alpha_x = (1-beta)*(xB-xA) + beta*(xD-xC)
        alpha_y = (1-beta)*(yB-yA) + beta*(yD-yC)
        beta_x  = (1-alpha)*(xC-xA) + alpha*(xD-xB)
        beta_y  = (1-alpha)*(yC-yA) + alpha*(yD-yB)
        
        # Invert the delta translation matrix into x,y --> alpha,beta
        det = alpha_x*beta_y - beta_x*alpha_y
        #x_alpha = beta_y/det
        #x_beta  = -alpha_y/det
        y_alpha = -beta_x/det
        y_beta  = alpha_x/det
        
        # Calculate the derivative of f w.r.t. alpha and beta
        dfda = (1-beta)*(fB-fA) + beta*(fD-fC)
        dfdb = (1-alpha)*(fC-fA) + alpha*(fD-fB)
        
        # Calculate the derivative with respect to x (and return it)
        dfdy = y_alpha*dfda + y_beta*dfdb
        return dfdy
        
        
if __name__ == '__main__':       
    print("Sorry, HARKinterpolation doesn't actually do much on its own.")
    print("To see some examples of its interpolation methods in action, look at any")
    print("of the model modules in /ConsumptionSavingModel.  In the future, running")
    print("this module will show examples of each interpolation class.")
    
    from time import clock
    import matplotlib.pyplot as plt
    
    RNG = np.random.RandomState(123)
    
    if False:
        x = np.linspace(1,20,39)
        y = np.log(x)
        dydx = 1.0/x
        f = CubicInterp(x,y,dydx)
        x_test = np.linspace(0,30,200)
        y_test = f(x_test)
        plt.plot(x_test,y_test)
        plt.show()
    
    if False:
        f = lambda x,y : 3.0*x**2.0 + x*y + 4.0*y**2.0
        dfdx = lambda x,y : 6.0*x + y
        dfdy = lambda x,y : x + 8.0*y
        
        y_list = np.linspace(0,5,100,dtype=float)
        xInterpolators = []
        xInterpolators_alt = []
        for y in y_list:
            this_x_list = np.sort((RNG.rand(100)*5.0))
            this_interpolation = LinearInterp(this_x_list,f(this_x_list,y*np.ones(this_x_list.size)))
            that_interpolation = CubicInterp(this_x_list,f(this_x_list,y*np.ones(this_x_list.size)),dfdx(this_x_list,y*np.ones(this_x_list.size)))
            xInterpolators.append(this_interpolation)
            xInterpolators_alt.append(that_interpolation)
        g = LinearInterpOnInterp1D(xInterpolators,y_list)
        h = LinearInterpOnInterp1D(xInterpolators_alt,y_list)
        
        rand_x = RNG.rand(100)*5.0
        rand_y = RNG.rand(100)*5.0
        z = (f(rand_x,rand_y) - g(rand_x,rand_y))/f(rand_x,rand_y)
        q = (dfdx(rand_x,rand_y) - g.derivativeX(rand_x,rand_y))/dfdx(rand_x,rand_y)
        r = (dfdy(rand_x,rand_y) - g.derivativeY(rand_x,rand_y))/dfdy(rand_x,rand_y)
        #print(z)
        #print(q)
        #print(r)
        
        z = (f(rand_x,rand_y) - g(rand_x,rand_y))/f(rand_x,rand_y)
        q = (dfdx(rand_x,rand_y) - g.derivativeX(rand_x,rand_y))/dfdx(rand_x,rand_y)
        r = (dfdy(rand_x,rand_y) - g.derivativeY(rand_x,rand_y))/dfdy(rand_x,rand_y)
        print(z)
        #print(q)
        #print(r)
    
    
    if False:
        f = lambda x,y,z : 3.0*x**2.0 + x*y + 4.0*y**2.0 - 5*z**2.0 + 1.5*x*z
        dfdx = lambda x,y,z : 6.0*x + y + 1.5*z
        dfdy = lambda x,y,z : x + 8.0*y
        dfdz = lambda x,y,z : -10.0*z + 1.5*x
        
        y_list = np.linspace(0,5,51,dtype=float)
        z_list = np.linspace(0,5,51,dtype=float)
        xInterpolators = []
        for y in y_list:
            temp = []
            for z in z_list:
                this_x_list = np.sort((RNG.rand(100)*5.0))
                this_interpolation = LinearInterp(this_x_list,f(this_x_list,y*np.ones(this_x_list.size),z*np.ones(this_x_list.size)))
                temp.append(this_interpolation)
            xInterpolators.append(deepcopy(temp))
        g = BilinearInterpOnInterp1D(xInterpolators,y_list,z_list)
        
        rand_x = RNG.rand(1000)*5.0
        rand_y = RNG.rand(1000)*5.0
        rand_z = RNG.rand(1000)*5.0
        z = (f(rand_x,rand_y,rand_z) - g(rand_x,rand_y,rand_z))/f(rand_x,rand_y,rand_z)
        q = (dfdx(rand_x,rand_y,rand_z) - g.derivativeX(rand_x,rand_y,rand_z))/dfdx(rand_x,rand_y,rand_z)
        r = (dfdy(rand_x,rand_y,rand_z) - g.derivativeY(rand_x,rand_y,rand_z))/dfdy(rand_x,rand_y,rand_z)
        p = (dfdz(rand_x,rand_y,rand_z) - g.derivativeZ(rand_x,rand_y,rand_z))/dfdz(rand_x,rand_y,rand_z)
        z.sort()
    
    
    
    if False:
        f = lambda w,x,y,z : 4.0*w*z - 2.5*w*x + w*y + 6.0*x*y - 10.0*x*z + 3.0*y*z - 7.0*z + 4.0*x + 2.0*y - 5.0*w
        dfdw = lambda w,x,y,z : 4.0*z - 2.5*x + y - 5.0
        dfdx = lambda w,x,y,z : -2.5*w + 6.0*y - 10.0*z + 4.0
        dfdy = lambda w,x,y,z : w + 6.0*x + 3.0*z + 2.0
        dfdz = lambda w,x,y,z : 4.0*w - 10.0*x + 3.0*y - 7
        
        x_list = np.linspace(0,5,16,dtype=float)
        y_list = np.linspace(0,5,16,dtype=float)
        z_list = np.linspace(0,5,16,dtype=float)
        wInterpolators = []
        for x in x_list:
            temp = []
            for y in y_list:
                temptemp = []
                for z in z_list:
                    this_w_list = np.sort((RNG.rand(16)*5.0))
                    this_interpolation = LinearInterp(this_w_list,f(this_w_list,x*np.ones(this_w_list.size),y*np.ones(this_w_list.size),z*np.ones(this_w_list.size)))
                    temptemp.append(this_interpolation)
                temp.append(deepcopy(temptemp))
            wInterpolators.append(deepcopy(temp))
        g = TrilinearInterpOnInterp1D(wInterpolators,x_list,y_list,z_list)
        
        N = 20000
        rand_w = RNG.rand(N)*5.0
        rand_x = RNG.rand(N)*5.0
        rand_y = RNG.rand(N)*5.0
        rand_z = RNG.rand(N)*5.0
        t_start = clock()
        z = (f(rand_w,rand_x,rand_y,rand_z) - g(rand_w,rand_x,rand_y,rand_z))/f(rand_w,rand_x,rand_y,rand_z)
        q = (dfdw(rand_w,rand_x,rand_y,rand_z) - g.derivativeW(rand_w,rand_x,rand_y,rand_z))/dfdw(rand_w,rand_x,rand_y,rand_z)
        r = (dfdx(rand_w,rand_x,rand_y,rand_z) - g.derivativeX(rand_w,rand_x,rand_y,rand_z))/dfdx(rand_w,rand_x,rand_y,rand_z)
        p = (dfdy(rand_w,rand_x,rand_y,rand_z) - g.derivativeY(rand_w,rand_x,rand_y,rand_z))/dfdy(rand_w,rand_x,rand_y,rand_z)
        s = (dfdz(rand_w,rand_x,rand_y,rand_z) - g.derivativeZ(rand_w,rand_x,rand_y,rand_z))/dfdz(rand_w,rand_x,rand_y,rand_z)
        t_end = clock()
        
        z.sort()
        print(z)
        print(t_end-t_start)
    
    if False:
        f = lambda x,y : 3.0*x**2.0 + x*y + 4.0*y**2.0
        dfdx = lambda x,y : 6.0*x + y
        dfdy = lambda x,y : x + 8.0*y
        
        x_list = np.linspace(0,5,101,dtype=float)
        y_list = np.linspace(0,5,101,dtype=float)
        x_temp,y_temp = np.meshgrid(x_list,y_list,indexing='ij')
        g = BilinearInterp(f(x_temp,y_temp),x_list,y_list)
        
        rand_x = RNG.rand(100)*5.0
        rand_y = RNG.rand(100)*5.0
        z = (f(rand_x,rand_y) - g(rand_x,rand_y))/f(rand_x,rand_y)
        q = (f(x_temp,y_temp) - g(x_temp,y_temp))/f(x_temp,y_temp)
        #print(z)
        #print(q)
        
        
    if False:
        f = lambda x,y,z : 3.0*x**2.0 + x*y + 4.0*y**2.0 - 5*z**2.0 + 1.5*x*z
        dfdx = lambda x,y,z : 6.0*x + y + 1.5*z
        dfdy = lambda x,y,z : x + 8.0*y
        dfdz = lambda x,y,z : -10.0*z + 1.5*x
        
        x_list = np.linspace(0,5,11,dtype=float)
        y_list = np.linspace(0,5,11,dtype=float)
        z_list = np.linspace(0,5,101,dtype=float)
        x_temp,y_temp,z_temp = np.meshgrid(x_list,y_list,z_list,indexing='ij')
        g = TrilinearInterp(f(x_temp,y_temp,z_temp),x_list,y_list,z_list)
        
        rand_x = RNG.rand(1000)*5.0
        rand_y = RNG.rand(1000)*5.0
        rand_z = RNG.rand(1000)*5.0
        z = (f(rand_x,rand_y,rand_z) - g(rand_x,rand_y,rand_z))/f(rand_x,rand_y,rand_z)
        q = (dfdx(rand_x,rand_y,rand_z) - g.derivativeX(rand_x,rand_y,rand_z))/dfdx(rand_x,rand_y,rand_z)
        r = (dfdy(rand_x,rand_y,rand_z) - g.derivativeY(rand_x,rand_y,rand_z))/dfdy(rand_x,rand_y,rand_z)
        p = (dfdz(rand_x,rand_y,rand_z) - g.derivativeZ(rand_x,rand_y,rand_z))/dfdz(rand_x,rand_y,rand_z)
        p.sort()    
        plt.plot(p)
        
        
    if False:
        f = lambda w,x,y,z : 4.0*w*z - 2.5*w*x + w*y + 6.0*x*y - 10.0*x*z + 3.0*y*z - 7.0*z + 4.0*x + 2.0*y - 5.0*w
        dfdw = lambda w,x,y,z : 4.0*z - 2.5*x + y - 5.0
        dfdx = lambda w,x,y,z : -2.5*w + 6.0*y - 10.0*z + 4.0
        dfdy = lambda w,x,y,z : w + 6.0*x + 3.0*z + 2.0
        dfdz = lambda w,x,y,z : 4.0*w - 10.0*x + 3.0*y - 7
        
        w_list = np.linspace(0,5,16,dtype=float)
        x_list = np.linspace(0,5,16,dtype=float)
        y_list = np.linspace(0,5,16,dtype=float)
        z_list = np.linspace(0,5,16,dtype=float)
        w_temp,x_temp,y_temp,z_temp = np.meshgrid(w_list,x_list,y_list,z_list,indexing='ij')
        mySearch = lambda trash,x : np.floor(x/5*32).astype(int)
        g = QuadlinearInterp(f(w_temp,x_temp,y_temp,z_temp),w_list,x_list,y_list,z_list)
        
        N = 1000000
        rand_w = RNG.rand(N)*5.0
        rand_x = RNG.rand(N)*5.0
        rand_y = RNG.rand(N)*5.0
        rand_z = RNG.rand(N)*5.0
        t_start = clock()
        z = (f(rand_w,rand_x,rand_y,rand_z) - g(rand_w,rand_x,rand_y,rand_z))/f(rand_w,rand_x,rand_y,rand_z)
        t_end = clock()
        #print(z)
        print(t_end-t_start)
    
    
    if False:
        f = lambda x,y : 3.0*x**2.0 + x*y + 4.0*y**2.0
        dfdx = lambda x,y : 6.0*x + y
        dfdy = lambda x,y : x + 8.0*y
        
        warp_factor = 0.01
        x_list = np.linspace(0,5,71,dtype=float)
        y_list = np.linspace(0,5,51,dtype=float)
        x_temp,y_temp = np.meshgrid(x_list,y_list,indexing='ij')
        x_adj = x_temp + warp_factor*(RNG.rand(x_list.size,y_list.size) - 0.5)
        y_adj = y_temp + warp_factor*(RNG.rand(x_list.size,y_list.size) - 0.5)
        g = Curvilinear2DInterp(f(x_adj,y_adj),x_adj,y_adj)
        
        rand_x = RNG.rand(1000)*5.0
        rand_y = RNG.rand(1000)*5.0
        t_start = clock()
        z = (f(rand_x,rand_y) - g(rand_x,rand_y))/f(rand_x,rand_y)
        q = (dfdx(rand_x,rand_y) - g.derivativeX(rand_x,rand_y))/dfdx(rand_x,rand_y)
        r = (dfdy(rand_x,rand_y) - g.derivativeY(rand_x,rand_y))/dfdy(rand_x,rand_y)
        t_end = clock()
        z.sort()
        q.sort()
        r.sort()
        #print(z)
        print(t_end-t_start)
        
        
    if False:
        f = lambda x,y,z : 3.0*x**2.0 + x*y + 4.0*y**2.0 - 5*z**2.0 + 1.5*x*z
        dfdx = lambda x,y,z : 6.0*x + y + 1.5*z
        dfdy = lambda x,y,z : x + 8.0*y
        dfdz = lambda x,y,z : -10.0*z + 1.5*x
        
        warp_factor = 0.01
        x_list = np.linspace(0,5,11,dtype=float)
        y_list = np.linspace(0,5,11,dtype=float)
        z_list = np.linspace(0,5,101,dtype=float)
        x_temp,y_temp = np.meshgrid(x_list,y_list,indexing='ij')
        xyInterpolators = []
        for j in range(z_list.size):
            x_adj = x_temp + warp_factor*(RNG.rand(x_list.size,y_list.size) - 0.5)
            y_adj = y_temp + warp_factor*(RNG.rand(x_list.size,y_list.size) - 0.5)
            z_temp = z_list[j]*np.ones(x_adj.shape)
            thisInterp = Curvilinear2DInterp(f(x_adj,y_adj,z_temp),x_adj,y_adj)
            xyInterpolators.append(thisInterp)
        g = LinearInterpOnInterp2D(xyInterpolators,z_list)
        
        N = 1000
        rand_x = RNG.rand(N)*5.0
        rand_y = RNG.rand(N)*5.0
        rand_z = RNG.rand(N)*5.0
        z = (f(rand_x,rand_y,rand_z) - g(rand_x,rand_y,rand_z))/f(rand_x,rand_y,rand_z)
        p = (dfdz(rand_x,rand_y,rand_z) - g.derivativeZ(rand_x,rand_y,rand_z))/dfdz(rand_x,rand_y,rand_z)
        p.sort()
        plt.plot(p)
        
        
    if False:
        f = lambda w,x,y,z : 4.0*w*z - 2.5*w*x + w*y + 6.0*x*y - 10.0*x*z + 3.0*y*z - 7.0*z + 4.0*x + 2.0*y - 5.0*w
        dfdw = lambda w,x,y,z : 4.0*z - 2.5*x + y - 5.0
        dfdx = lambda w,x,y,z : -2.5*w + 6.0*y - 10.0*z + 4.0
        dfdy = lambda w,x,y,z : w + 6.0*x + 3.0*z + 2.0
        dfdz = lambda w,x,y,z : 4.0*w - 10.0*x + 3.0*y - 7
        
        warp_factor = 0.1
        w_list = np.linspace(0,5,16,dtype=float)
        x_list = np.linspace(0,5,16,dtype=float)
        y_list = np.linspace(0,5,16,dtype=float)
        z_list = np.linspace(0,5,16,dtype=float)
        w_temp,x_temp = np.meshgrid(w_list,x_list,indexing='ij')
        wxInterpolators = []
        for i in range(y_list.size):
            temp = []
            for j in range(z_list.size):
                w_adj = w_temp + warp_factor*(RNG.rand(w_list.size,x_list.size) - 0.5)
                x_adj = x_temp + warp_factor*(RNG.rand(w_list.size,x_list.size) - 0.5)
                y_temp = y_list[i]*np.ones(w_adj.shape)
                z_temp = z_list[j]*np.ones(w_adj.shape)
                thisInterp = Curvilinear2DInterp(f(w_adj,x_adj,y_temp,z_temp),w_adj,x_adj)
                temp.append(thisInterp)
            wxInterpolators.append(temp)
        g = BilinearInterpOnInterp2D(wxInterpolators,y_list,z_list)
        
        N = 1000000
        rand_w = RNG.rand(N)*5.0
        rand_x = RNG.rand(N)*5.0
        rand_y = RNG.rand(N)*5.0
        rand_z = RNG.rand(N)*5.0
        
        t_start = clock()
        z = (f(rand_w,rand_x,rand_y,rand_z) - g(rand_w,rand_x,rand_y,rand_z))/f(rand_w,rand_x,rand_y,rand_z)
        t_end = clock()
        z.sort()
        print(z)
        print(t_end-t_start)
        
        
