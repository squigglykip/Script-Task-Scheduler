# Task Scheduler TODO List

## Critical Bugs
- [ ] Fix config.json file access in packaged exe
  - Issue: Add Task function not saving to config in exe version
  - Reference: gui.py lines 269-274 and main.py lines 41-60

## Features & Enhancements
- [ ] Add system tray functionality
  - Minimize to tray
  - Right-click menu for basic controls
- [ ] Add task categories/tags for better organization
- [ ] Implement task priority levels
- [ ] Add task execution history view
- [ ] Create backup/restore functionality for config
- [ ] Add task import/export feature

## Testing
- [ ] Create unit tests
  - Task scheduling logic
  - Config file operations
  - GUI components
- [ ] Integration tests
  - Full task execution workflow
  - Config file updates
  - Log file operations
- [ ] Cross-platform testing
  - Windows
  - Linux
  - MacOS
- [ ] Edge case testing
  - Invalid file paths
  - Malformed config files
  - Network paths
  - Special characters in task names

## Documentation
- [ ] Add inline code documentation
- [ ] Create developer setup guide
- [ ] Document build process
- [ ] Add troubleshooting guide for common issues
- [ ] Create user manual with screenshots

## Security
- [ ] Implement input validation
- [ ] Add file path sanitization
- [ ] Implement logging security best practices
- [ ] Add error handling for file permissions

## Performance
- [ ] Profile memory usage
- [ ] Optimize log file handling
- [ ] Review thread management
- [ ] Implement log rotation

## Build & Deployment
- [ ] Create automated build script
- [ ] Set up CI/CD pipeline
- [ ] Create installer package
- [ ] Add version checking/updates
- [ ] Test packaged exe thoroughly

## Code Quality
- [ ] Add type hints
- [ ] Implement error handling best practices
- [ ] Add code comments
- [ ] Review naming conventions
- [ ] Implement logging best practices

## Future Considerations
- [ ] Web interface
- [ ] Remote management capability
- [ ] Email notifications
- [ ] Task dependencies
- [ ] API integration capabilities
