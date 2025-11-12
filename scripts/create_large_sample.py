#!/usr/bin/env python3
"""
Create Large Sample Dataset — Generate substantial sample data for testing
"""

import json
import random
from pathlib import Path

# Sample Wikipedia articles covering various domains
WIKIPEDIA_ARTICLES = [
    # Mathematics
    {"title": "Mathematics", "text": "Mathematics is the study of numbers, quantities, and shapes. It includes algebra, geometry, calculus, and many other branches. Mathematics is used in science, engineering, and many other fields."},
    {"title": "Algebra", "text": "Algebra is a branch of mathematics that uses symbols and letters to represent numbers and quantities in formulas and equations. It includes linear algebra, abstract algebra, and many other subfields."},
    {"title": "Geometry", "text": "Geometry is the branch of mathematics concerned with shapes, sizes, and properties of space. It includes Euclidean geometry, non-Euclidean geometry, and differential geometry."},
    {"title": "Calculus", "text": "Calculus is the mathematical study of continuous change. It includes differential calculus and integral calculus. Calculus is fundamental to physics, engineering, and many sciences."},
    
    # Physics
    {"title": "Physics", "text": "Physics is the natural science that studies matter, motion, and behavior through space and time. It includes mechanics, thermodynamics, quantum mechanics, and many other branches."},
    {"title": "Quantum Mechanics", "text": "Quantum mechanics is a fundamental theory in physics that describes the physical properties of nature at the scale of atoms and subatomic particles. It includes wave-particle duality and uncertainty principle."},
    {"title": "Thermodynamics", "text": "Thermodynamics is the branch of physics that deals with heat, work, and temperature. It includes the laws of thermodynamics and entropy."},
    {"title": "Electromagnetism", "text": "Electromagnetism is a branch of physics involving the study of electromagnetic force. It includes electricity, magnetism, and electromagnetic radiation."},
    
    # Biology
    {"title": "Biology", "text": "Biology is the study of living organisms. It includes cell biology, genetics, evolution, ecology, and many other branches. Biology helps us understand life on Earth."},
    {"title": "Genetics", "text": "Genetics is the study of genes, genetic variation, and heredity in organisms. It includes molecular genetics, population genetics, and medical genetics."},
    {"title": "Evolution", "text": "Evolution is the change in heritable characteristics of biological populations over successive generations. It includes natural selection, genetic drift, and mutation."},
    {"title": "Ecology", "text": "Ecology is the study of interactions among organisms and their environment. It includes population ecology, community ecology, and ecosystem ecology."},
    
    # Chemistry
    {"title": "Chemistry", "text": "Chemistry is the study of matter and its properties. It includes organic chemistry, inorganic chemistry, physical chemistry, and analytical chemistry."},
    {"title": "Organic Chemistry", "text": "Organic chemistry is the study of carbon-containing compounds. It includes the structure, properties, and reactions of organic molecules."},
    {"title": "Biochemistry", "text": "Biochemistry is the study of chemical processes within living organisms. It includes metabolism, enzyme function, and molecular biology."},
    
    # Computer Science
    {"title": "Computer Science", "text": "Computer science is the study of computation and information processing. It includes algorithms, data structures, programming languages, and artificial intelligence."},
    {"title": "Algorithm", "text": "An algorithm is a step-by-step procedure for solving a problem or accomplishing a task. Algorithms are fundamental to computer science and programming."},
    {"title": "Artificial Intelligence", "text": "Artificial intelligence is the simulation of human intelligence by machines. It includes machine learning, neural networks, and natural language processing."},
    
    # History
    {"title": "World War II", "text": "World War II was a global war that lasted from 1939 to 1945. It involved most of the world's nations and resulted in significant changes to global politics and society."},
    {"title": "Renaissance", "text": "The Renaissance was a period of cultural rebirth in Europe from the 14th to the 17th century. It included advances in art, science, and literature."},
    {"title": "Industrial Revolution", "text": "The Industrial Revolution was a period of major industrialization from the 18th to 19th century. It transformed economies and societies through new manufacturing processes."},
    
    # Geography
    {"title": "Europe", "text": "Europe is a continent located entirely in the Northern Hemisphere. It includes many countries with diverse cultures, languages, and histories."},
    {"title": "Asia", "text": "Asia is the largest continent by land area. It includes many countries with diverse cultures, from Japan to India to the Middle East."},
    {"title": "Africa", "text": "Africa is the second-largest continent. It includes many countries with rich histories and diverse cultures."},
    
    # Philosophy
    {"title": "Philosophy", "text": "Philosophy is the study of fundamental questions about existence, knowledge, values, reason, and language. It includes ethics, metaphysics, and epistemology."},
    {"title": "Ethics", "text": "Ethics is the branch of philosophy that studies moral principles and values. It includes questions about right and wrong, good and evil."},
    {"title": "Logic", "text": "Logic is the study of correct reasoning. It includes formal logic, symbolic logic, and mathematical logic."},
    
    # Medicine
    {"title": "Medicine", "text": "Medicine is the science and practice of diagnosing, treating, and preventing disease. It includes many specialties like cardiology, neurology, and surgery."},
    {"title": "Anatomy", "text": "Anatomy is the study of the structure of living organisms. It includes human anatomy, comparative anatomy, and microscopic anatomy."},
    {"title": "Physiology", "text": "Physiology is the study of how living organisms function. It includes human physiology, plant physiology, and animal physiology."},
    
    # More diverse topics
    {"title": "Literature", "text": "Literature is written works, especially those considered to have artistic or intellectual value. It includes novels, poetry, drama, and essays."},
    {"title": "Art", "text": "Art is the expression of human creative skill and imagination. It includes painting, sculpture, music, and many other forms."},
    {"title": "Music", "text": "Music is an art form that uses sound and silence. It includes many genres and styles from classical to modern."},
    {"title": "Economics", "text": "Economics is the study of how societies allocate scarce resources. It includes microeconomics, macroeconomics, and international economics."},
    {"title": "Psychology", "text": "Psychology is the scientific study of mind and behavior. It includes cognitive psychology, developmental psychology, and clinical psychology."},
    {"title": "Sociology", "text": "Sociology is the study of society and social behavior. It includes the study of social institutions, social change, and social problems."},
]

# Sample book excerpts
BOOK_EXCERPTS = [
    "The Art of War by Sun Tzu. War is a matter of vital importance to the state. It is a matter of life and death, a road either to safety or to ruin. Hence it is a subject of inquiry which can on no account be neglected. The art of war is governed by five constant factors. These are: the Moral Law, Heaven, Earth, the Commander, and Method and Discipline.",
    
    "The Prince by Niccolò Machiavelli. It is better to be feared than loved, if you cannot be both. For men have less scruple in offending one who is beloved than one who is feared, for love is preserved by the link of obligation which, owing to the baseness of men, is broken at every opportunity for their advantage; but fear preserves you by a dread of punishment which never fails.",
    
    "The Republic by Plato. Justice is giving each man his due. The just man is the one who does his own work and does not meddle with what is not his own. The state is the individual writ large. As the individual has three parts—reason, spirit, and appetite—so the state has three classes—rulers, auxiliaries, and producers.",
    
    "On the Origin of Species by Charles Darwin. It is not the strongest of the species that survives, nor the most intelligent that survives. It is the one that is most adaptable to change. Natural selection acts by preserving and accumulating small inherited modifications.",
    
    "The Wealth of Nations by Adam Smith. The division of labor is the great cause of the increase in public opulence. It increases the productive powers of labor by allowing workers to specialize in particular tasks.",
    
    "Critique of Pure Reason by Immanuel Kant. All our knowledge begins with the senses, proceeds then to the understanding, and ends with reason. There is nothing higher than reason.",
    
    "Leviathan by Thomas Hobbes. In the state of nature, the life of man is solitary, poor, nasty, brutish, and short. To escape this, men form a social contract and establish a sovereign power.",
    
    "The Social Contract by Jean-Jacques Rousseau. Man is born free, and everywhere he is in chains. The social contract is an agreement among individuals to form a society and establish government.",
]

def create_large_wikipedia_sample(num_articles: int = 1000):
    """Create a large Wikipedia sample by duplicating and varying articles"""
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    output_file = data_dir / "wikipedia.jsonl"
    
    print(f"Creating {num_articles} Wikipedia articles...")
    
    articles = []
    base_articles = WIKIPEDIA_ARTICLES.copy()
    
    # Duplicate and vary articles
    for i in range(num_articles):
        base = random.choice(base_articles)
        # Create variation
        article = {
            "title": f"{base['title']} ({i % 10 + 1})",
            "text": base['text'] + f" This is article variation {i}. " + base['text'][:50] + "..."
        }
        articles.append(article)
        
        if (i + 1) % 100 == 0:
            print(f"  Created {i + 1} articles...")
    
    # Write to JSON Lines
    with open(output_file, 'w', encoding='utf-8') as f:
        for article in articles:
            json.dump(article, f, ensure_ascii=False)
            f.write('\n')
    
    print(f"✓ Created {len(articles)} Wikipedia articles in {output_file}")
    print(f"  File size: {output_file.stat().st_size / 1024:.1f} KB")

def create_large_books_sample(num_chunks: int = 500):
    """Create a large BooksCorpus sample"""
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    output_file = data_dir / "books.txt"
    
    print(f"\nCreating {num_chunks} book chunks...")
    
    chunks = []
    base_excerpts = BOOK_EXCERPTS.copy()
    
    for i in range(num_chunks):
        base = random.choice(base_excerpts)
        # Create variation
        chunk = f"{base} [Chunk {i}] " + base[:100] + "\n\n"
        chunks.append(chunk)
        
        if (i + 1) % 100 == 0:
            print(f"  Created {i + 1} chunks...")
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(chunks))
    
    print(f"✓ Created {len(chunks)} book chunks in {output_file}")
    print(f"  File size: {output_file.stat().st_size / 1024:.1f} KB")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--wikipedia", type=int, default=1000, help="Number of Wikipedia articles")
    parser.add_argument("--books", type=int, default=500, help="Number of book chunks")
    args = parser.parse_args()
    
    print("=" * 60)
    print("Creating Large Sample Dataset")
    print("=" * 60)
    
    create_large_wikipedia_sample(args.wikipedia)
    create_large_books_sample(args.books)
    
    print("\n" + "=" * 60)
    print("✓ Sample Dataset Ready")
    print("=" * 60)
    print("\nFiles created:")
    print(f"  - data/wikipedia.jsonl ({args.wikipedia} articles)")
    print(f"  - data/books.txt ({args.books} chunks)")
    print("\nYou can now run:")
    print("  python3 scripts/ingest_bert_data.py")

if __name__ == "__main__":
    main()

