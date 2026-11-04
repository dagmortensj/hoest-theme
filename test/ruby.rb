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

# Vanskelige tilfeller: operatoroverlasting, blokker, symboler, strenger og mønstre
class Vektor
  attr_reader :x, :y
  def initialize(x = 0, y = 0) = (@x, @y = x, y)
  def +(annen) = Vektor.new(x + annen.x, y + annen.y)
  def *(k) = Vektor.new(x * k, y * k)
  def -@ = Vektor.new(-x, -y)
  def [](i) = i.zero? ? x : y
  def ==(annen) = x == annen.x && y == annen.y
  def coerce(tall) = [Vektor.new(tall, tall), self]
  def to_s = "a + b == c #{x} #{y > 0 ? 'opp' : 'ned'} \t\u00e6" + 'apostrof \'x\' #{ikke}' + %q(rå #{x}) + %w[a b].join
end
def vanskelig(navn = nil, *rest, nøkkel: 1, **valg, &blokk)
  t = 0; t += 1; t -= 2; t *= 3; t /= 4; t %= 5; t **= 2; t <<= 1; t |= 1; t ^= 2; t &= ~3; t ||= 0; t &&= 1
  lik = t == 1 || t.eql?(1) && t != nil and t <=> 2 or !t ^ t === 3; neg = -t + +t % 2 ** 3
  v = Vektor.new(1, 2) + Vektor.new(3, 4) * 2 + -Vektor.new; v2 = 2 * v; lik &&= v == v2 && v[0] != v[1]
  (1..10).step(2) { |i| next if i.between?(3, 7) || (1...3) === i; redo if false }
  tekst = <<~TEKST
    Her-dokument med #{navn} og \t #{blokk&.call(t) || valg.fetch(:x, 0)}
  TEKST
  case [navn, rest]
  in [String => n, [Integer => første, *]] if n.start_with?("J") then puts n, første
  in {navn: String} | nil then nil
  else raise NotImplementedError, "#{navn.inspect} #{rest.size} #{nøkkel}"
  end
  lambda { |a, b = 1| a + b }.(1, 2) + proc { |a| a }.call(1) + ->(a) { a }[1] + yield(t) + neg + tekst.size
end
