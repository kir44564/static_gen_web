from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links
from split_nodes import split_nodes_delimiter


def split_nodes_image(old_nodes):

    new_nodes = []
    
    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        
        images = extract_markdown_images(node.text)
        
        
        if not images:
            new_nodes.append(node)
            continue
        
        
        current_text = node.text
        for image_alt, image_url in images:
            
            markdown = f"![{image_alt}]({image_url})"
            parts = current_text.split(markdown, 1)
            
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            
            current_text = parts[1] if len(parts) > 1 else ""
        
        
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):

    new_nodes = []
    
    for node in old_nodes:
        
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        
        links = extract_markdown_links(node.text)
        
        
        if not links:
            new_nodes.append(node)
            continue
        
        
        current_text = node.text
        for link_text, link_url in links:
            
            markdown = f"[{link_text}]({link_url})"
            parts = current_text.split(markdown, 1)
            
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            
            
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            
            current_text = parts[1] if len(parts) > 1 else ""
        
        
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def text_to_textnodes(text):

    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    nodes = split_nodes_image(nodes)

    nodes = split_nodes_link(nodes)
    
    return nodes