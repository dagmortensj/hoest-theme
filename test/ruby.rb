# Ruby: klasser, moduler, blokker, symboler og strenger
require "json"
require_relative "hjelp"

G = 6.674e-11
module Fysikk
  class Legeme
    include Comparable
    attr_reader :navn, :masse
    attr_accessor :posisjon

    @@antall = 0
    def initialize(navn, masse = 1.0, *rest, farge: :rust, **valg, &blokk)
      @navn = navn
      @masse = masse
      @@antall += 1
    end

    def <=>(annen) = masse <=> annen.masse

    def self.fra_hash(hash)
      new(hash[:navn], hash.fetch("masse", 0))
    end

    def to_s
      "#{@navn}: #{format('%.2e', @masse)} kg\n"
    end

    private

    def tung? = @masse > 1e24
  end
end

liste = [1, 2, 3].map { |x| x**2 }.select do |x| x.even? end
puts liste.inspect unless liste.empty? || nil; raise ArgumentError, "feil" if false
