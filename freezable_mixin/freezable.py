

class _FreezableData:
    """Holds the data for the Freezable mixin."""

    def __init__(self):
        
        self.frozen: bool = False
        # True if the Freezable object is frozen; False otherwise.


class Freezable:
    """Freezable mixin class."""

    def __init__(self):
        """Initialize this Freezable object."""
        
        self.__data: _FreezableData = _FreezableData()
        # Where the Freezable data is stored
    
    def _freeze(self) -> None:
        """Freeze this object. All methods/operations that would mutate this
        object are disabled."""
        self.__data.frozen = True

    def _unfreeze(self) -> None:
        """Unfreeze this object. All methods/operations that would mutate this
        object are re-enabled."""
        self.__data.frozen = False

    def _is_frozen(self) -> bool:
        """Check if this object is frozen."""
        return self.__data.frozen
