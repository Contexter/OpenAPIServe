import Foundation

/// A `DataProvider` that reads data from a file.
public struct FileDataProvider: DataProvider {
    private let filePath: String

    public init(filePath: String) {
        self.filePath = filePath
    }

    public func getData() -> String {
        do {
            let data = try String(contentsOfFile: filePath, encoding: .utf8)
            return data
        } catch {
            print("Error reading file at \(filePath): \(error)")
            return ""
        }
    }
}
