import Vision
import Foundation

let arguments = CommandLine.arguments
if arguments.count < 2 { exit(1) }
let imagePath = arguments[1]
let url = URL(fileURLWithPath: imagePath)

guard let cgImageSource = CGImageSourceCreateWithURL(url as CFURL, nil),
      let cgImage = CGImageSourceCreateImageAtIndex(cgImageSource, 0, nil) else { exit(1) }

let requestHandler = VNImageRequestHandler(cgImage: cgImage, options: [:])

let request = VNRecognizeTextRequest { request, error in
    guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
    var fullText = ""
    for observation in observations {
        guard let candidate = observation.topCandidates(1).first else { continue }
        fullText += candidate.string + "\n"
    }
    print(fullText)
}

request.recognitionLevel = .accurate
try? requestHandler.perform([request])
