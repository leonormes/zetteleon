
## Formalized State Machine (STATE_DOCKED)

The system now exposes an explicit state variable for inspection.

### Verification
1. **Docked Mode**:
   ```bash
   echo $STATE_DOCKED
   # Expected: 1
   ```
2. **Mobile Mode**:
   ```bash
   # (Simulate by renaming PROJECT_ROOT or unmounting)
   echo $STATE_DOCKED
   # Expected: 0
   ```
