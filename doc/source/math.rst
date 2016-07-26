Math of texmex
==============

Some of the code deals with math, which I think will be a lot clearer if I explain it as math
first, and then as code.

The probability mass function
-----------------------------

The Poisson-lognormal pmf is a convolution of the Poisson pmf with the lognormal pdf:

.. math::

   \mathrm{Poilog}(n; \mu, \sigma) &= \int_0^\infty \mathrm{Poisson}(n; \lambda) \times \mathrm{Lognormal}(\lambda; \mu, \sigma) \,\mathrm{d}\lambda \\
   &= \int_0^\infty \frac{\lambda^n e^{-\lambda}}{n!} \times \frac{1}{\lambda \sigma \sqrt{2 \pi}} \exp \left\{ -\frac{(\ln \lambda - \mu)^2}{2 \sigma^2} \right\} \,\mathrm{d}\lambda \\
   &= \frac{1}{n! \, \sigma \sqrt{2\pi}} \int_{-\infty}^\infty \exp \left\{ nx - e^x - \frac{1}{2} \left(\frac{x - \mu}{\sigma}\right)^2 \right\} \,\mathrm{d}x,

where :math:`n` is the number of reads, :math:`\mu` and :math:`\sigma` are the distribution's location and
shape parameters, :math:`\lambda` is the "true abundance", and :math:`x = \ln \lambda` is a change of variables.

This integral presents two challenges. First, when :math:`n` is large, :math:`n!` becomes intractable.
Second, when :math:`x` is large, the double exponential becomes intractable.

Thankfully, the integral has some nice features: the integrand has a single maximum, and it falls away
from the maximum in a reliable way, so we can get around these problems. First, instead of computing
:math:`n!`, I compute :math:`\log n!`, i.e., :math:`\log \Gamma (n + 1)`, which is tractable, and put
that value inside the exponential integrand. Second, I try to compute the bounds of the numerical 
integral intelligently.

Specifically, I examine the three terms inside the integral:

.. math::

   f(x) \equiv nx - e^x - \frac{1}{2} \left( \frac{x - \mu}{\sigma} \right)^2

It is easy to numerically compute the :math:`x^\star` that maximizes :math:`f`. To find a good lower
bound, I establish some threshold :math:`T` (say, :math:`10^{-10}`) and iterate:

1. Guess a difference :math:`\Delta x`, say :math:`1.0`.
2. If :math:`f(x^\star - \Delta x) / f(x^\star) < T`, then the lower bound :math:`x^\star - \Delta x` is far
   enough away from :math:`x^\star` that integrating down to that point will capture most of integral.
3. If the ratio is not low enough, multiply :math:`\Delta x` by some factor, say :math:`2.0`, and try again.

To find the upper bound, repeat but with :math:`x^\star + \Delta x`.

Maximum likelihood estimation
-----------------------------
I use two tricks here. First, because :math:`\sigma` must be nonnegative, I perform the optimization over
:math:`(\mu, \log \sigma)`, which is unconstrained, then convert back to :math:`\sigma` after the optimization
is complete.

Second, I try to pick smart initial conditions. Good guesses for :math:`\mu` and :math:`\sigma` are, I think,
just the mean and standard deviation of the logarithms of the data themselves, i.e., the maximum likelihood
estimates of those parameters for the vanilla lognormal distribution. This works most of the time. In the R
package, I found I had to do some mild grid-searching to get good fits for all my samples. In that case,
I searched with :math:`\sigma` fixed at :math:`1.0` and I ran fits with :math:`\mu \in \{-2.0, -1.0, 0.0, 1.0, 2.0\}`.
Usually the first or second attempt worked; I never had a case where none of the fits worked.
