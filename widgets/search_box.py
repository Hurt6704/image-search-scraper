from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QSpinBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from widgets import DeleteButton, DirectorySelector, SearchButton, TextBox

class SearchBox(QGroupBox):
    """
    Groupbox widget layout for a search API client's queries
    """
    delete = pyqtSignal()
    def __init__(self, maxResults: int, title: str, saveDirectory: str, parent: QWidget = None):
        super().__init__(title, parent)
        self.setContentsMargins(11, 3, 3, 11)
        self.deleteInProgress = False

        # Main vertical layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Delete button and its layout
        deleteLayout = QHBoxLayout()
        deleteLayout.setAlignment(Qt.AlignRight)
        deleteLayout.setContentsMargins(0, 6, 0, 0)
        self.deleteButton = DeleteButton()
        deleteLayout.addWidget(self.deleteButton)
        self.mainLayout.addLayout(deleteLayout)

        # Search query layout
        searchLayout = QHBoxLayout()
        self.searchTextBox = TextBox('Enter your search query here...')
        self.searchButton = SearchButton()
        searchLayout.addWidget(self.searchTextBox)
        searchLayout.addWidget(self.searchButton)
        searchLayout.addStretch(1)
        self.mainLayout.addLayout(searchLayout)

        # Number of images
        numImagesLayout = QHBoxLayout()
        self.numImages = QSpinBox()
        self.numImages.setRange(1, maxResults)
        self.numImages.setValue(1)
        numImagesLayout.addWidget(QLabel('Number of images'))
        numImagesLayout.addWidget(self.numImages)
        numImagesLayout.addStretch(1)
        self.mainLayout.addLayout(numImagesLayout)

        # Save directory
        self.saveDir = DirectorySelector(saveDirectory)
        self.mainLayout.addWidget(self.saveDir)

        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        # Connect signals and slots
        self.deleteButton.clicked.connect(self.destroy)
    
    def saveDirectory(self):
        return self.saveDir.selectedDirectory()

    def numberOfImages(self):
        return self.numImages.value()

    def searchQuery(self):
        return self.searchTextBox.toPlainText()

    def setSaveDirectory(self, directory: str):
        self.saveDir.setSelectedDirectory(directory)

    def setProperties(self, title: str, marginLeft: int = 11,
                      marginTop: int = 3, marginRight: int = 3, marginBottom: int = 11):
        self.setTitle(title)
        # Also set the contents margins since setting the title seems to change the values initially defined (bug?)
        self.setContentsMargins(marginLeft, marginTop, marginRight, marginBottom)

    def _clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self._clearLayout(item.layout())

    @pyqtSlot()
    def destroy(self):
        self.deleteInProgress = True
        # Delete all items in the main layout
        self._clearLayout(self.mainLayout)
        # Delete self
        self.deleteLater()
        self.delete.emit()