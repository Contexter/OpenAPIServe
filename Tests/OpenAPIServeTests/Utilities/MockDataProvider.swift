import Vapor
import OpenAPIServe

struct MockDataProvider: DataProvider {
    let mockContent: String

    func getData() -> String {
        return mockContent
    }

    static func openAPI30() -> MockDataProvider {
        return MockDataProvider(mockContent: "openapi: 3.0.0")
    }

    static func openAPI31() -> MockDataProvider {
        return MockDataProvider(mockContent: "openapi: 3.1.0")
    }
}
