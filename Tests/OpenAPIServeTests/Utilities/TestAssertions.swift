import XCTVapor

struct TestAssertions {
    static func assertOKResponse(
        _ response: XCTHTTPResponse,
        contains expectedContent: String
    ) {
        XCTAssertEqual(response.status, .ok)
        XCTAssertTrue(response.body.string.contains(expectedContent))
    }
}
