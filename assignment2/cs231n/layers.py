import numpy as np

def affine_forward(x, w, b):
  """
  Computes the forward pass for an affine (fully-connected) layer.

  The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
  examples, where each example x[i] has shape (d_1, ..., d_k). We will
  reshape each input into a vector of dimension D = d_1 * ... * d_k, and
  then transform it to an output vector of dimension M.

  Inputs:
  - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
  - w: A numpy array of weights, of shape (D, M)
  - b: A numpy array of biases, of shape (M,)
  
  Returns a tuple of:
  - out: output, of shape (N, M)
  - cache: (x, w, b)
  """
  out = None
  #############################################################################
  # TODO: Implement the affine forward pass. Store the result in out. You     #
  # will need to reshape the input into rows.                                 #
  #############################################################################
  N = x.shape[0]
  D = np.prod(x.shape[1:])
  #this should be the same as w.shape[0]
  M = b.shape[0]

  out = np.dot(x.reshape(N,D), w.reshape(D,M)) + b.reshape(-1)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b)
  return out, cache

def affine_backward(dout, cache):
  """
  Computes the backward pass for an affine layer.

  Inputs:
  - dout: Upstream derivative, of shape (N, M)
  - cache: Tuple of:
    - x: Input data, of shape (N, d_1, ... d_k)
    - w: Weights, of shape (D, M)

  Returns a tuple of:
  - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
  - dw: Gradient with respect to w, of shape (D, M)
  - db: Gradient with respect to b, of shape (M,)
  """
  x, w, b = cache
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the affine backward pass.                                 #
  #############################################################################
  # N = x.shape[0]
  # D = w.shape[0]
  # M = w.shape[1]

  N = x.shape[0]
  D = np.prod(x.shape[1:])
  M = b.shape[0]

  #has to involve equal dimensions of w and dout
  dx = np.dot( dout, w.reshape(D,M).T).reshape(x.shape)
  #has to involve x and dout (only one combination makes sensed)
  dw = np.dot( x.reshape(N, D).T, dout).reshape(w.shape)

  #shape has to be same as b
  db = np.sum(dout, axis=0)

  # assert dx.shape == x.shape
  # assert dw.reshape(w.shape).shape == w.shape
  # assert db.shape == b.shape
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


# _relu_forward = lambda y: y*(y>0)
# vect_relu_forward = np.vectorize(_relu_forward)
# def f():
#     x = np.random.randn(500,500)
#     x = vect_relu_forward(x)
#     #print(np.mean(x))

# def g():
#     y = np.random.randn(500,500)
#     y = np.maximum(0,y)
#     #print(np.mean(y))

# def time_diff():
#     f_times = []
#     g_times = []
#     f()
#     g()
#     for i in range(100):
#         start = time.time()
#         g()
#         f_times.append(time.time() - start)
#         start = time.time()
#         f()
#         g_times.append(time.time() - start)
#     print(np.mean(f_times))
#     print(np.mean(g_times))

# time_diff()

def continuous_appx_relu_forward(x, alpha = 1):
  out = None
  out = np.log(1 + np.exp(alpha * x))
  return out, (x,alpha)

def continuous_appx_relu_backward(dout, cache):
  dx = None
  x, alpha = cache
  return alpha * dout / (1 + np.exp(alpha * x))
  #modified logistic function

def leaky_relu_forward(x, alpha):
  """
  Computes the forward pass for a layer of leaky rectified linear units (l-ReLUs).

  Input:
  - x: Inputs, of any shape
  - alpha: scale parameter > 0

  Returns a tuple of:
  - out: Output, of the same shape as x
  - cache: x
  """
  out = None

  #leaky_relu
  out_p = np.maximum(0, x)

  #this needs to broadcast
  out_n = np.maximum(0, -a*x)
  out = out_p + out_n

  cache = x, a
  return out, cache


def leaky_relu_backward(dout, cache):
  """
  Computes the backward pass for a layer of leaky rectified linear units (l-ReLUs).

  Input:
  - dout: Upstream derivatives, of any shape
  - cache: Input x, of same shape as dout

  Returns:
  - dx: Gradient with respect to x
  """
  dx = None
  x, a = cache
  #############################################################################
  # TODO: Implement the ReLU backward pass.                                   #
  #############################################################################
  dx = np.array(dout, copy=True)
  dx_p = dx[ x > 0]
  dx_n = dx[ x < 0] * alpha

  dx = dx_p + dx_n
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def relu_forward(x):
  """
  Computes the forward pass for a layer of rectified linear units (ReLUs).

  Input:
  - x: Inputs, of any shape

  Returns a tuple of:
  - out: Output, of the same shape as x
  - cache: x
  """
  out = None
  #############################################################################
  # TODO: Implement the ReLU forward pass.                                    #
  #############################################################################
  out = np.maximum(0, x)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = x
  return out, cache

def relu_backward(dout, cache):
  """
  Computes the backward pass for a layer of rectified linear units (ReLUs).

  Input:
  - dout: Upstream derivatives, of any shape
  - cache: Input x, of same shape as dout

  Returns:
  - dx: Gradient with respect to x
  """
  dx, x = None, cache
  #############################################################################
  # TODO: Implement the ReLU backward pass.                                   #
  #############################################################################
  dx = np.array(dout, copy=True)
  dx[ x < 0] = 0
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx

def batchnorm_forward(x, gamma, beta, bn_param):
  """
  Forward pass for batch normalization.
  
  During training the sample mean and (uncorrected) sample variance are
  computed from minibatch statistics and used to normalize the incoming data.
  During training we also keep an exponentially decaying running mean of the mean
  and variance of each feature, and these averages are used to normalize data
  at test-time.

  At each timestep we update the running averages for mean and variance using
  an exponential decay based on the momentum parameter:

  running_mean = momentum * running_mean + (1 - momentum) * sample_mean
  running_var = momentum * running_var + (1 - momentum) * sample_var

  Note that the batch normalization paper suggests a different test-time
  behavior: they compute sample mean and variance for each feature using a
  large number of training images rather than using a running average. For
  this implementation we have chosen to use running averages instead since
  they do not require an additional estimation step; the torch7 implementation
  of batch normalization also uses running averages.

  Input:
  - x: Data of shape (N, D)
  - gamma: Scale parameter of shape (D,)
  - beta: Shift paremeter of shape (D,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features

  Returns a tuple of:
  - out: of shape (N, D)
  - cache: A tuple of values needed in the backward pass
  """
  mode = bn_param['mode']
  eps  = bn_param.get('eps', 1e-5)
  momentum = bn_param.get('momentum', 0.9)

  N, D = x.shape
  running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
  running_var  = bn_param.get('running_var', np.ones(D, dtype=x.dtype))

  out, cache, x_hat = None, None, None
  mean = x.mean(axis=0)
  var  = x.var(axis=0)

  if mode == 'train':
    #############################################################################
    # TODO: Implement the training-time forward pass for batch normalization.   #
    # Use minibatch statistics to compute the mean and variance, use these      #
    # statistics to normalize the incoming data, and scale and shift the        #
    # normalized data using gamma and beta.                                     #
    #                                                                           #
    # You should store the output in the variable out. Any intermediates that   #
    # you need for the backward pass should be stored in the cache variable.    #
    #                                                                           #
    # You should also use your computed sample mean and variance together with  #
    # the momentum variable to update the running mean and running variance,    #
    # storing your result in the running_mean and running_var variables.        #
    #############################################################################
    running_mean = momentum * mean + (1 - momentum) * running_mean
    running_var  = momentum * var + (1 - momentum) * running_var
    x_hat = (x - mean) / np.sqrt(var + eps)
    x = gamma * x_hat + beta
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  elif mode == 'test':
    #############################################################################
    # TODO: Implement the test-time forward pass for batch normalization. Use   #
    # the running mean and variance to normalize the incoming data, then scale  #
    # and shift the normalized data using gamma and beta. Store the result in   #
    # the out variable.                                                         #
    #############################################################################
    x_hat = (x - running_mean / np.sqrt(running_var + eps))
    x = gamma * (x_hat - running_mean) / np.sqrt(running_var + eps) + beta
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  else:
    raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

  # Store the updated running means back into bn_param
  bn_param['running_mean'] = running_mean
  bn_param['running_var'] = running_var
  out = x
  cache = (gamma, beta, x_hat, mean, var)
  return out, cache


def batchnorm_backward(dout, cache):
  """
  Backward pass for batch normalization.
  
  For this implementation, you should write out a computation graph for
  batch normalization on paper and propagate gradients backward through
  intermediate nodes.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, D)
  - cache: Variable of intermediates from batchnorm_forward.
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs x, of shape (N, D)
  - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
  - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
  """
  dx, dgamma, dbeta = None, None, None
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #############################################################################
  gamma, beta, x_hat, mu, var = cache
  m = dout.shape[0]
  sigma  = np.sqrt(var)
  dbeta  = np.sum(dout, axis=0)
  dgamma = np.diag(np.dot(x_hat.T,dout))
  dx_hat = gamma * dout

  dvar   = -0.5 * np.sum(dx_hat * x_hat, axis=0) / var
  dmean  = -1. *  np.sum(dx_hat, axis=0)/sigma

  dx     = dx_hat / sigma + dvar * 2 * x_hat * sigma / m + dmean / m
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dgamma, dbeta


def batchnorm_backward_alt(dout, cache):
  """
  Alternative backward pass for batch normalization.
  
  For this implementation you should work out the derivatives for the batch
  normalizaton backward pass on paper and simplify as much as possible. You
  should be able to derive a simple expression for the backward pass.
  
  Note: This implementation should expect to receive the same cache variable
  as batchnorm_backward, but might not use all of the values in the cache.
  
  Inputs / outputs: Same as batchnorm_backward
  """
  dx, dgamma, dbeta = None, None, None
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #                                                                           #
  # After computing the gradient with respect to the centered inputs, you     #
  # should be able to compute gradients with respect to the inputs in a       #
  # single statement; our implementation fits on a single 80-character line.  #
  #############################################################################
  g, beta, x_hat, mu, var = cache
  m = dout.shape[0]
  dbeta, dgamma = np.sum(dout, axis=0), np.diag(np.dot(x_hat.T,dout))

  sigma  = np.sqrt(var)
  dbeta  = np.sum(dout, axis=0)
  dgamma = np.diag(np.dot(x_hat.T,dout))
  dx_hat = g * dout

  dx = np.zeros(dout.shape)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  
  return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
  """
  Performs the forward pass for (inverted) dropout.

  Inputs:
  - x: Input data, of any shape
  - dropout_param: A dictionary with the following keys:
    - p: Dropout parameter. We drop each neuron output with probability p.
    - mode: 'test' or 'train'. If the mode is train, then perform dropout;
      if the mode is test, then just return the input.
    - seed: Seed for the random number generator. Passing seed makes this
      function deterministic, which is needed for gradient checking but not in
      real networks.

  Outputs:
  - out: Array of the same shape as x.
  - cache: A tuple (dropout_param, mask). In training mode, mask is the dropout
    mask that was used to multiply the input; in test mode, mask is None.
  """
  p, mode = dropout_param['p'], dropout_param['mode']
  if 'seed' in dropout_param:
    np.random.seed(dropout_param['seed'])

  mask = None
  out = None

  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase forward pass for inverted dropout.   #
    # Store the dropout mask in the mask variable.                            #
    ###########################################################################
    #mask = np.random.choice([0., 1.], size=(x.shape), replace=True, p=[p,1-p]) / p
    mask = (np.random.rand(*x.shape) < p ) / p
    #time the comparison of these should be done
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    ###########################################################################
    # TODO: Implement the test phase forward pass for inverted dropout.       #
    ###########################################################################
    mask = np.ones(x.shape)
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

  out = x * mask
  cache = (dropout_param, mask)
  out = out.astype(x.dtype, copy=False)

  return out, cache


def dropout_backward(dout, cache):
  """
  Perform the backward pass for (inverted) dropout.

  Inputs:
  - dout: Upstream derivatives, of any shape
  - cache: (dropout_param, mask) from dropout_forward.
  """
  dropout_param, mask = cache
  mode = dropout_param['mode']
  
  dx = None
  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase backward pass for inverted dropout.  #
    ###########################################################################
    dx = mask * dout
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    dx = dout
  return dx


def conv_forward_naive(x, w, b, conv_param):
  """
  A naive implementation of the forward pass for a convolutional layer.

  The input consists of N data points, each with C channels, height H and width
  W. We convolve each input with F different filters, where each filter spans
  all C channels and has height HH and width HH.

  Input:
  - x: Input data of shape (N, C, H, W)
  - w: Filter weights of shape (F, C, HH, WW)
  - b: Biases, of shape (F,)
  - conv_param: A dictionary with the following keys:
    - 'stride': The number of pixels between adjacent receptive fields in the
      horizontal and vertical directions.
    - 'pad': The number of pixels that will be used to zero-pad the input.

  Returns a tuple of:
  - out: Output data, of shape (N, F, H', W') where H' and W' are given by
    H' = 1 + (H + 2 * pad - HH) / stride
    W' = 1 + (W + 2 * pad - WW) / stride
  - cache: (x, w, b, conv_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the convolutional forward pass.                           #
  # Hint: you can use the function np.pad for padding.                        #
  #############################################################################
  N, C, H, W   = x.shape
  F, _, HH, WW = w.shape

  pad    = int(conv_param['pad'])
  stride = int(conv_param['stride'])

  height = int(1 + (H + 2 * pad - HH) / stride)
  width  = int(1 + (W + 2 * pad - WW) / stride)

  out = np.zeros((N,F, height, width))

  padded_x = np.pad(x, ((0,0),(0,0),(pad,pad),(pad,pad)), 'constant')
  # np.pad(input, (padding_1, padding_2, padding_3, padding_4), 'constant')
  #where padding is a tuple, (before_size, after_size)
  #  np.pad(np.array([1 2 3]), (0,1))
  # (0,1)
  # print(np.pad(np.array([1,2,3]), (0,1), 'constant'))
  # [1 2 3 0]
  # print(np.pad(np.array([1,2,3]), (1,1), 'constant'))
  # [0 1 2 3 0]
  #print(w[0][0])
  #filters are 2d arrays at each w[i][j], 0<= i <= w.shape[0], 0<= j <= w.shape[1]
  # print(np.tile(w[0][0],(2,2)).shape)
  # print(x[0][0].shape)

  for i in range(0,N):
    for j in range(0,F):
      for k in range(0,height):
        hs = k * stride
        for l in range(0,width):
          ws = l * stride
          window = padded_x[i, :, hs:hs+HH, ws:ws+WW]
          out[i,j,k,l] = np.sum(window * w[j]) + b[j]

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b, conv_param)
  return out, cache


def conv_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a convolutional layer.

  Inputs:
  - dout: Upstream derivatives.
  - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

  Returns a tuple of:
  - dx: Gradient with respect to x
  - dw: Gradient with respect to w
  - db: Gradient with respect to b
  """
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the convolutional backward pass.                          #
  #############################################################################
  x, w, b, conv_param = cache
  N, C, H, W   = x.shape
  F, _, HH, WW = w.shape

  pad    = int(conv_param['pad'])
  stride = int(conv_param['stride'])

  height = int(1 + (H + 2 * pad - HH) / stride)
  width  = int(1 + (W + 2 * pad - WW) / stride)

  dx = np.zeros(x.shape)
  dw = np.zeros(w.shape)
  db = np.zeros(b.shape)

  padded_x  = np.pad(x, ((0,0),(0,0),(pad,pad),(pad,pad)), 'constant')
  padded_dx = np.pad(dx, ((0,0),(0,0),(pad,pad),(pad,pad)), 'constant')

  for i in range(N):
    for j in range(F):
      for k in range(0,height):
        hs = k * stride
        for l in range(0,width):
          ws = l * stride
          window = padded_x[i, :, hs:hs+HH, ws:ws+WW]

          # out[i,j,k,l] = np.sum(window * w[j]) + b[j]
          db[j] += dout[i,j,k,l]
          dw[j] += window * dout[i, j, k, l]
          padded_dx[i, :, hs:hs+HH, ws:ws+WW] += w[j] * dout[i, j, k, l]

  dx = padded_dx[:, :, pad:pad+H, pad:pad+W]
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def max_pool_forward_naive(x, pool_param):
  """
  A naive implementation of the forward pass for a max pooling layer.

  Inputs:
  - x: Input data, of shape (N, C, H, W)
  - pool_param: dictionary with the following keys:
    - 'pool_height': The height of each pooling region
    - 'pool_width': The width of each pooling region
    - 'stride': The distance between adjacent pooling regions

  Returns a tuple of:
  - out: Output data
  - cache: (x, pool_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the max pooling forward pass                              #
  #############################################################################
  pool_height = pool_param['pool_height']
  pool_width  = pool_param['pool_width']
  stride = pool_param['stride']

  N, C, H, W = x.shape
  height = int(1 + (H - pool_height) / stride)
  width  = int(1 + (W - pool_width) / stride)

  out = np.zeros((N,C,height,width))

  for i in range(N):
    for j in range(C):
      for k in range(height):
        hs = k * stride
        for l in range(width):
          ws = l * stride
          window = x[i,j,hs:hs+pool_height,ws:ws+pool_width]
          out[i,j,k,l] = np.max(window)

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, pool_param)
  return out, cache


def max_pool_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a max pooling layer.

  Inputs:
  - dout: Upstream derivatives
  - cache: A tuple of (x, pool_param) as in the forward pass.

  Returns:
  - dx: Gradient with respect to x
  """
  dx = None
  #############################################################################
  # TODO: Implement the max pooling backward pass                             #
  #############################################################################
  x, pool_param = cache
  HH = pool_param['pool_height']
  WW = pool_param['pool_width']
  stride = pool_param['stride']
  N, C, H, W = x.shape
  Hp = 1 + (H - HH) / stride
  Wp = 1 + (W - WW) / stride

  dx = np.zeros_like(x)

  for i in range(N):
    for j in range(C):
      for k in range(int(Hp)):
        hs = k * stride
        for l in range(int(Wp)):
          ws = l * stride

          # Window (C, HH, WW)
          window = x[i, j, hs:hs+HH, ws:ws+WW]
          m = np.max(window)

          # Gradient of max is indicator
          dx[i, j, hs:hs+HH, ws:ws+WW] += (window == m) * dout[i, j, k, l]
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
  """
  Computes the forward pass for spatial batch normalization.
  
  Inputs:
  - x: Input data of shape (N, C, H, W)
  - gamma: Scale parameter, of shape (C,)
  - beta: Shift parameter, of shape (C,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance. momentum=0 means that
      old information is discarded completely at every time step, while
      momentum=1 means that new information is never incorporated. The
      default of momentum=0.9 should work well in most situations.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features
    
  Returns a tuple of:
  - out: Output data, of shape (N, C, H, W)
  - cache: Values needed for the backward pass
  """
  out, cache = None, None

  #############################################################################
  # TODO: Implement the forward pass for spatial batch normalization.         #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  N, C, H, W = x.shape
  D = H * W

  mode = bn_param['mode']
  eps  = bn_param.get('eps', 1e-5)
  momentum = bn_param.get('momentum', 0.9)

  x = x.reshape(N, C, H * W)
  running_mean = bn_param.get('running_mean', np.zeros((C,D), dtype=x.dtype))
  running_var  = bn_param.get('running_var', np.ones((C,D), dtype=x.dtype))

  mean = np.zeros((C,D))
  var  = np.zeros((C,D))

  for i in range(C):
    mean[i] = x[:,i].mean(axis=(0))
    var[i]  = x[:,i].var(axis=(0))
  #print(mean.shape)
  #axis=(0, 2, 3)

  x_hat = np.zeros((N,C,D))

  if mode == 'train':
    out = np.zeros((N,C,D))
    for i in range(C):
      bn_param_c = {}
      x[:,i,:], cache = batchnorm_forward(x[:,i,:], gamma[i], beta[i], bn_param)
      x_hat[:,i,:] = cache[2]
      gamma[i] = cache[0]
      beta[i]  = cache[1]
      running_mean[i] = momentum * mean[i] + (1 - momentum) * running_mean[i]
      running_var[i]  = momentum * var[i] + (1 - momentum) * running_var[i]

  elif mode == 'test':
    for i in range(C):
      x_hat[:,i,:] = (x[:,i,:] - running_mean[i]) / np.sqrt(running_var[i] + eps)
      x[:,i,:] = gamma[i] * x_hat[:,i,:] + beta[i]

  else:
    raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

  # Store the updated running means back into bn_param
  #bn_param['running_mean'] = {}
  #bn_param['running_mean'][color] = running_mean[color]
  #bn_param['running_var'][color] = running_mean[color]
  #cache = (x for k,x in cache_color.items())

  bn_param['running_mean'] = running_mean
  bn_param['running_var']  = running_var
  out   = x.reshape(N, C, H, W)
  cache = (gamma, beta, x_hat, mean, var)

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return out, cache


def spatial_batchnorm_backward(dout, cache):
  """
  Computes the backward pass for spatial batch normalization.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, C, H, W)
  - cache: Values from the forward pass
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs, of shape (N, C, H, W)
  - dgamma: Gradient with respect to scale parameter, of shape (C,)
  - dbeta: Gradient with respect to shift parameter, of shape (C,)
  """
  #FIRST attempt
  #NOT WORKING PROPERLY
  #
  # IS THERE an issue with the shape of the expected outputs?
  # probably an issue with the bn_param in an earlier step
  # NEED to calculate backpropagated result(?)
  dx, dgamma, dbeta = None, None, None
  gamma, beta, x_hat, mean, var = cache

  N, C, H, W = dout.shape
  dx     = np.zeros((dout.shape))
  dgamma = np.zeros_like(gamma)
  dbeta  = np.zeros_like(beta)
  for i in range(gamma.shape[0]):
    dout_c  = dout[:,i,:,:].reshape(N, H * W)
    cache_c = (gamma[i], beta[i], x_hat[:,i], mean[i], var[i])
    dx_tmp, dgamma_tmp, dbeta_tmp = batchnorm_backward(dout_c, cache_c)
    #batchnorm_backwards returns dgamma_tmp.shape = (D,)
    #                            dbeta_tmp.shape  = (D,)
    #return dx, dgamma, dbeta
    dx[:,i]   = dx_tmp.reshape(N,H,W)
    dgamma[i] = np.mean(dgamma_tmp)
    dbeta[i]  = np.mean(dbeta_tmp)

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta

def svm_loss(x, y):
  """
  Computes the loss and gradient using for multiclass SVM classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  N = x.shape[0]
  correct_class_scores = x[np.arange(N), y]
  margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
  margins[np.arange(N), y] = 0
  loss = np.sum(margins) / N
  num_pos = np.sum(margins > 0, axis=1)
  dx = np.zeros_like(x)
  dx[margins > 0] = 1
  dx[np.arange(N), y] -= num_pos
  dx /= N
  return loss, dx


def softmax_loss(x, y):
  """
  Computes the loss and gradient for softmax classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  probs = np.exp(x - np.max(x, axis=1, keepdims=True))
  probs /= np.sum(probs, axis=1, keepdims=True)
  N = x.shape[0]
  loss = -np.sum(np.log(probs[np.arange(N), y] + 1e-16)) / N
  dx = probs.copy()
  dx[np.arange(N), y] -= 1
  dx /= N
  return loss, dx
