# TESTING.md

*Package Maintainers!*
This document describes testing procedures for the software contained in this
repository. All sections must be completed and signed off before a package can
be moved from one repository to the next.

## Part 1: Staging -> Proposed
* Did it build?
* Are files present in build package:
    - Check package, data.tar - make sure all files intended to be installed are
      there

## Part 2: Proposed -> Stable

All advertised functionality must be present and functional. 
Things to check for correct function:

* Install `software-properties-gtk` from apt, if not installed.
* Settings Tab: 
  1. Disable all checkmarks listed in both standard and developer options
  2. Launch `software-properties-gtk` and check that all sources are disabled
     * Four main repos are in "Ubuntu Software" Tab
     * Source Code is in "Ubuntu Software" Tab
     * Pre-release updates is in "Developer Options" tab
     * `software-properties-gtk` must now be closed.
  3. Enable all source checkmarks in both standard and developer options
  4. Launch `software-properties-gtk` and check that all sources are enabled
     * Same places as before.
     * Remember to close `software-properties-gtk`
* Updates Tab:
  1. Disable all update repos in Updates Tab
  2. Launch `software-properties-gtk` and check that all sources are disabled
     * All repos are in "Updates" tab.
     * Close `software-properties-gtk` now.
  3. Enable all update repos in Updates Tab
  4. Launch `software-properties-gtk` and check that all sources are enabled
     * Same places, close when finished.
* Extra Sources Tab:
  1. Click "Add" (+) button at bottom.
     * "Add Source" dialog appears
     * "Add" button is grayed out.
  2. Add extra repository (e.g. `ppa:kernelstub/daily`)
     * "Add" button is enabled when valid ppa is typed in.
     * Repository is added to list after breif update
  3. Double-click repository; check that Edit Dialog opens; close it.
     * "Modify Source" button opens.
     * "Cancel" button in top left.
     * Green "Save" button in top right.
     * "Remove Source" button, red, is at bottom left.
  4. Set "Version" to `xenial`
  5. Set "Type" to `Source Code`
  6. Click "Save".
     * Dialog closes
     * Repository is updated in list after a short delay.
  7. Click same repository.
  8. Click "Edit" (pencil) button 
     * "Modify Source" opens again.
  9. Change "Version" to `xebiak`
  10. Click "Save"
      * Repository is updated after delay.
      * Error message appears: "Does not have a Release File"
  11. Click Close
  12. Double-click same repository
      * "Modify Source" opens again.
  13. Change "Version" to xenial
  14. Turn off "Enabled" Switch
  15. Click "Save"
      * Repository is updated and moved to disabled section below.
      * Repository is not bold
      * "_(disabled)_" is appended to end of repository
  16. Double-click same repository
      * "Modify Source" opens again.
  17. Click "Remove source"
      * "Remove Source" confirmation dialog opens.
      * "Cancel button" in top left
      * Red "Remove" button in top right.
  18. Click "Remove"
      * Repository disappears from list after short delay.
  19. Double-Click "Pop-OS" Repository.
      * "Modify Source" opens again.
  20. Click "Remove Source"
      * "Remove Source" dialog opens again.
  21. Click "Cancel"
      * "Remove Source" dialog closes.
      * "Modify Source" dialog remains open.
  22. Click "Cancel"
      * "Modify Source" dialog closes.
      * "Pop-OS" repository remains in list.
  
