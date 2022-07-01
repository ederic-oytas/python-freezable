
from functools import wraps
from typing import Callable, TypeVar


_F = TypeVar('_F', bound=Callable)
# Type variable for a Callable. This is used instead of just Callable so that
# the function signature can be preserved.


class _FreezableData:
    """Holds the data for the Freezable mixin."""

    def __init__(self):
        """Create a _FreezableData object."""
        
        self.frozen: bool = False
        # True if the Freezable object is frozen; False otherwise.


class FrozenError(RuntimeError):
    """Raised when an operation that could mutate a Freezable object
    is used when that object is frozen."""


class Freezable:
    """Freezable mixin class."""

    def __init__(self):
        """Initialize this Freezable object."""
        
        self._Freezable__data: _FreezableData
        object.__setattr__(self, '_Freezable__data', _FreezableData())
        # Data for the Freezable mixin. This attribute is considered to be
        # private.
        # The name is already mangled so that the type checker will be okay
        # with functions outside of the class accessing this attribute.
        # `object.__setattr__` is used instead of setting it directly in the
        # case that __setattr__ is overridden.
    
    #
    # Freezing Methods
    #
    
    def _freeze(self) -> None:
        """Freeze this object. All methods/operations that could mutate this
        object are disabled."""
        self._Freezable__data.frozen = True

    def _unfreeze(self) -> None:
        """Unfreeze this object. All methods/operations that could mutate this
        object are re-enabled."""
        self._Freezable__data.frozen = False

    def _is_frozen(self) -> bool:
        """Check if this object is frozen."""
        return self._Freezable__data.frozen


def disabled_when_frozen(method: _F) -> _F:
    """Instance method decorator to throw a ``FrozenError`` if the object is
    frozen. The class must subclass ``Freezable``.
    """
    
    @wraps(method)
    def wrapped(self: Freezable, *args, **kwargs):
        if self._Freezable__data.frozen:
            if hasattr(method, '__name__'):
                raise FrozenError("cannot call method '%s' while object is "
                                  "frozen" % method.__name__)
            else:
                raise FrozenError("cannot call method while object is frozen")
        return method(self, *args, **kwargs)

    return wrapped  # type: ignore
