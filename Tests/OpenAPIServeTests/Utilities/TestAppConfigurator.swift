import Vapor
import OpenAPIServe

struct TestAppConfigurator {
    static func configureApp(
        with dataProvider: DataProvider
    ) -> Application {
        let app = Application(.testing)
        app.middleware.use(OpenAPIMiddleware(dataProvider: dataProvider))
        return app
    }
}
