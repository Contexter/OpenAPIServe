
import Vapor

/// Protocol for providing OpenAPI spec data.
public protocol DataProvider {
    func getData() -> String
}

/// Reads OpenAPI spec data from a file.
public struct FileDataProvider: DataProvider {
    private let filePath: String

    public init(filePath: String) {
        self.filePath = filePath
    }

    public func getData() -> String {
        guard let data = try? String(contentsOfFile: filePath) else {
            fatalError("Failed to read file at \(filePath)")
        }
        return data
    }
}

/// Middleware to serve OpenAPI specs.
public final class OpenAPIMiddleware: Middleware {
    private let dataProvider: DataProvider

    public init(dataProvider: DataProvider) {
        self.dataProvider = dataProvider
    }

    public func respond(to request: Request, chainingTo next: Responder) -> EventLoopFuture<Response> {
        if request.url.path == "/openapi.yml" {
            let spec = dataProvider.getData()
            let response = Response(status: .ok, body: .init(string: spec))
            response.headers.contentType = .init(type: "application", subType: "x-yaml")
            return request.eventLoop.makeSucceededFuture(response)
        }
        return next.respond(to: request)
    }
}
