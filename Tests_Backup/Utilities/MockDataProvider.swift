
import OpenAPIServe

// MockDataProvider conforming to DataProvider protocol
public struct MockDataProvider: DataProvider {
    public let mockContent: String
    public init(mockContent: String) {
        self.mockContent = mockContent
    }
    public func getData() -> String {
        return mockContent
    }
}
