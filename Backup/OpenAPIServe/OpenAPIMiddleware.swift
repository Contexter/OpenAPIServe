import Vapor

public struct OpenAPIMiddleware: Middleware {
    private let filePath: String

    public init(filePath: String) {
        self.filePath = filePath
    }

    public func respond(to request: Request, chainingTo next: Responder) -> EventLoopFuture<Response> {
        if request.url.path == "/openapi.yml" {
            let file = request.application.directory.resourcesDirectory + filePath
            print("Looking for file at:", file)
            print("File exists:", FileManager.default.fileExists(atPath: file))
            if FileManager.default.fileExists(atPath: file) {
                return request.eventLoop.makeSucceededFuture(
                    request.fileio.streamFile(at: file)
                )
            } else {
                return request.eventLoop.makeSucceededFuture(
                    Response(status: .notFound, body: Response.Body(string: "File not found"))
                )
            }
        } else {
            return next.respond(to: request)
        }
    }
}
