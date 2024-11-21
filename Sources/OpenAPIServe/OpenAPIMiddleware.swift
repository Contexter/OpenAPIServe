import Vapor

/// Protocol for providing OpenAPI spec data.
public protocol DataProvider {
    func getData() -> String
}

/// Middleware to serve OpenAPI specifications.
public struct OpenAPIMiddleware: Middleware {
    private let dataProvider: DataProvider

    /// Initializes the middleware with a data provider.
    public init(dataProvider: DataProvider) {
        self.dataProvider = dataProvider
    }

    /// Handles incoming requests and serves the OpenAPI specification if requested.
    public func respond(to request: Request, chainingTo next: Responder) -> EventLoopFuture<Response> {
        if request.url.path == "/openapi.yml" {
            let data = dataProvider.getData()

            if data.isEmpty {
                let response = Response(status: .notFound)
                response.body = .init(string: "OpenAPI specification not found")
                return request.eventLoop.makeSucceededFuture(response)
            }

            let response = Response(status: .ok)
            response.headers.contentType = .init(type: "application", subType: "x-yaml")
            response.body = .init(string: data)
            return request.eventLoop.makeSucceededFuture(response)
        }

        return next.respond(to: request)
    }
}
